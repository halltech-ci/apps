# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"
    
    
    account_analytic_id = fields.Many2one('account.analytic.account', compute="_compute_analytic_account", store=True)
    account_analytic_id1 = fields.Many2one('account.analytic.account', string="Analytic Account")#Use to store analytic_account form purchase_order
    
    @api.depends('account_analytic_id1', 'project.analytic_account_id')
    def _compute_analytic_account(self):
        for request in self:
            if request.sale_order:
                request.account_analytic_id = request.project.analytic_account_id 
            else:
                request.account_analytic_id = request.account_analytic_id1
    
    @api.onchange('account_analytic_id')
    def _onchange_analytic_account(self):
        res = []
        for line in self.line_ids:
            if isinstance(line.id, int):
                res.append(
                    (1, line.id, {"analytic_account_id": self.analytic_account_id.id})
                )
            else:
                # this is new record, do nothing !
                return
        self.line_ids = res
            
            
class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'
    
    analytic_account_id = fields.Many2one('account.analytic.account', compute="_compute_analytic_account", store=True, readonly=True)
    
    @api.depends('request_id.account_analytic_id',)
    def _compute_analytic_account(self):
        """Propagate account_analytic from purchase_request to purchase line"""
        for line in self:
            if line.request_id.account_analytic_id:
                line.analytic_account_id = line.request_id.account_analytic_id
            else:
                return
            

    