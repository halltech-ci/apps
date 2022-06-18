# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    account_analytic_id = fields.Many2one('account.analytic.account')
    
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    account_analytic_id = fields.Many2one('account.analytic.account', compute="_compute_analytic_account")
    
    def _compute_analytic_account(self):
        for line in self:
            if line.order_id.account_analytic_id:
                line.account_analytic_id = line.order_id.account_analytic_id
            else:
                
                