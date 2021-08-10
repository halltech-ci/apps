# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"
     
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('waiting_for_approval', 'Waiting For Approval'),
        ('approve', 'Approved'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    def ask_for_approval(self):
        for rec in self:
            rec.state = 'waiting_for_approval'
    
    def action_approve(self):
        for rec in self:
            rec.state = 'approve'
    
    def action_quotation_send(self):
        super(SaleOrder,self).action_quotation_send()
        for rec in self:
            rec.state = 'sent'
    
    
 

