# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'
    
    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.da.sequence")
    

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
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
                order.write({'state': 'to approve',
                             'name':self.env['ir.sequence'].next_by_code('purchase.bc.sequence')
                            })
        return True