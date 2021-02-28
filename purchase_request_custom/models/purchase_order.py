# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    project_id = fields.Many2one('project.project', string='Project', readonly = True,
        default=lambda self: self.env['purchase.order.line'].search([('order_id', '=', self.id)], limit=1).project_id.code,
    )
    
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
    
    project_id = fields.Many2one('project.project', compute='_compute_project_id', string="Project")
    
    @api.depends('purchase_request_allocation_ids')
    def _compute_project_id(self):
        for rec in self:
            if rec.purchase_request_allocation_ids:
                allocation_ids = self.env['purchase.order.line'].search([], limit=1).mapped('purchase_request_allocation_ids')
                #allocation_ids = rec.mapped('purchase_request_allocation_ids') 
                #if len(allocation_ids) == 1:
                rec.project_id = allocation_ids.purchase_request_line_id.project or False
    
    