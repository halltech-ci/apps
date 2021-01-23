# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    etiquet_analytic_id = fields.Many2one("account.analytic.tag",string="Etiquette")
    
    account_account_id = fields.Many2one(related='etiquet_analytic_id.account_id',string="Account")
    
    
    
    


