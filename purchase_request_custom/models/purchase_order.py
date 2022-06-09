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
    state = fields.Selection(selection_add=[
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('order', 'Bon de commande'),
        ('to approve', 'To Approve'),
        ('purchase', 'Commande confirmee'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ])
    amount_due = fields.Float(compute='_compute_debit_limit', string="Solde Credit", store=True)
    
    @api.depends('partner_id.debit_limit', 'partner_id.debit')
    def _compute_debit_limit(self):
        for rec in self:
            rec.amount_due = rec.partner_id.debit_limit - rec.partner_id.debit
    
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
    
    def create_order(self):
        for order in self:
            order.write({'name':self.env['ir.sequence'].next_by_code('purchase.bc.sequence')})
            order.write({'state':'order'})
        return True
    
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent', 'order']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step'\
                    or (order.company_id.po_double_validation == 'two_step'\
                        and order.amount_total < self.env.company.currency_id._convert(
                            order.company_id.po_double_validation_amount, order.currency_id, order.company_id, order.date_order or fields.Date.today()))\
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
                #order.write({'name':self.env['ir.sequence'].next_by_code('purchase.bc.sequence')})
            else:
                order.write({'state': 'to approve'})
            #order.write({'name':self.env['ir.sequence'].next_by_code('purchase.bc.sequence')})
        return True
    
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    specifications = fields.Text(string="Specifications", compute="_compute_specifications",)
    project = fields.Many2one('project.project', compute="_compute_specifications")
    product_code = fields.Char(related="product_id.default_code", sting="Code Article")
    account_analytic_id = fields.Many2one('account.analytic.account', compute='_compute_specifications')
    
    def _compute_specifications(self):
        for line in self:
            #request_line = self.env['purchase.order.line'].search([])
            pr_line = line.mapped('purchase_request_lines').ids
            pr_obj = self.env['purchase.request.line'].browse()
            if len(pr_line) > 0:
                pr_obj = self.env['purchase.request.line'].browse(pr_line[0])
            line.project = pr_obj.project
            line.specifications = pr_obj.specifications
            line.account_analytic_id = pr_obj.analytic_account_id
            
    