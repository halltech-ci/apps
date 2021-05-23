# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"
     
    state = fields.Selection(selection_add=[
        ('waiting_for_approval', 'Waiting For Approval'),
        ('approve', 'Approved'),
        ('sent',),
        ]
    )
    
    def ask_for_approval(self):
        for rec in self:
            rec.state = 'waiting_for_approval'
    
    def action_approve(self):
        for rec in self:
            rec.state = 'approve'
    
    def action_quotation_send(self):
        res = super(SaleOrder,self).action_quotation_send()
        if res:
            for rec in self:
                rec.state = 'sent'
        return res
    
    
 

