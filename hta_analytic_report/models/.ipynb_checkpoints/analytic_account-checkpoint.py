# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticType(models.Model):
    _name = "account.analytic.type"
    _description = "Here we configure all analytic type to group analytic report based on it"
    
    name = fields.Char(required=True)
    account_id = fields.Many2one('account.account')
    
    
    
class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"
    
    analytic_type_id = fields.Many2one('account.analytic.type', string="Type")
    