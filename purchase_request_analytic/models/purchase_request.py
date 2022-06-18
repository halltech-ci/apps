# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"
    
    
    account_analytic_id = fields.Many2one('account.analytic.account', compute="_compute_analytic_account")
    account_analytic_id1 = fields.Many2one('account.analytic.account', string="Analytic Account")
    
    @api.depends('account_analytic_id1', 'project.analytic_account_id')
    def _compute_analytic_account(self):
        for request in self:
            request.account_analytic_id = request.project.analytic_account_id or request.analytic_account_id1
            
            
class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'
    
    analytic_account_id = fields.Many2one('account.analytic.account', compute="_compute_analytic_account")
    
    @api.depends('request_id.account_analytic_id')
    def _compute_analytic_account(self):
        for line in self:
            if line.request_id.account_analytic_id:
                line.analytic_account_id = line.request_id.account_analytic_id

    