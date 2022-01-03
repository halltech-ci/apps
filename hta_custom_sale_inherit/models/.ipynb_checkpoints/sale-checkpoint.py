# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    
    
    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms or ''
    
    sale_order_recipients = fields.Char("A l’attention de")
    note = fields.Text('Terms and conditions', default=_default_note, required=True)
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Terms', check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    
    payment_term_ids = fields.Selection([('1', 'Immediate Payment'),
                                  ('2', '30  jours'),
                                  ('3', '60  jours'),
                                  ('4', '90  jours'),
                                  ('5', '120  jours')])