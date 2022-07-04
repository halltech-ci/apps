# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    account_analytic_id = fields.Many2one('account.analytic.account')
    
    @api.onchange('account_analytic_id')
    def _onchange_analytic_account(self):
        res = []
        for line in self.order_line:
            if isinstance(line.id, int):
                res.append(
                    (1, line.id, {"analytic_account_id": self.analytic_account_id.id})
                )
            else:
                # this is new record, do nothing !
                return
        self.line_ids = res
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    account_analytic_id = fields.Many2one('account.analytic.account', compute="_compute_analytic_account", store=True)
    
    @api.depends('order_id.account_analytic_id')
    def _compute_analytic_account(self):
        for line in self:
            if line.order_id.account_analytic_id:
                line.account_analytic_id = line.order_id.account_analytic_id
            else:
                continue
                