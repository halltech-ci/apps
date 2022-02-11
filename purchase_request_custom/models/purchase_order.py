# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from num2words import num2words
from odoo.addons import decimal_precision as dp


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    #num2words convert number to word
    def _num_to_words(self, num):
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()
        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        num_to_word = _num2words(num, lang=lang.iso_code)
        return num_to_word
    
    def _compute_amount_to_word(self):
        for rec in self:
            rec.amount_to_word = str(self._num_to_words(rec.amount_total)).upper()
    
    
    amount_to_word = fields.Char(string="Amount In Words:", compute='_compute_amount_to_word')
    purchase_approver = fields.Many2one('res.users')
    
    @api.onchange('state')
    def _compute_purchase_approver(self):
        if self.state == 'approve':
            self.purchase_approver = self.user_id
    """
    def button_approve(self, force=False):
        self.write({'state': 'purchase', 'date_approve': fields.Datetime.now(), 'purchase_approver':self.user_id.id})
        self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        return {}
    """
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            company_id = vals.get("company_id", self.env.company.id)
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].with_context(force_company=company_id).next_by_code('purchase.dc.sequence', sequence_date=seq_date) or '/'
            
        return super(PurchaseOrder, self).create(vals)
    
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.company.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            order.write({'name':self.env['ir.sequence'].next_by_code('purchase.bc.sequence')})
        return True
    
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    specifications = fields.Text(string="Specifications",
                                compute="_compute_specifications"
                                )
    project = fields.Many2one('project.project', compute="_compute_specifications")
    
    
    def _compute_specifications(self):
        for line in self:
            if line.purchase_request_lines:
                pr_line= line.purchase_request_lines.ids[0]
                purchase_request = self.env['purchase.request.line'].search([('id', '=', pr_line)], limit=1)
                line.project = purchase_request.project
                line.specifications = purchase_request.specifications
            else:
                return
            
            
    """
    @api.depends('purchase_request_lines')
    def _compute_project_id(self):
        for line in self:
            line.project = line.purchase_request_lines.project
    """
    
    