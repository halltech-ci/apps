# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move.line"
    
    etiquet_analytic_id = fields.Many2one("account.analytic.tag",string="Etiquette", store=True)
    
    
    
    
    


