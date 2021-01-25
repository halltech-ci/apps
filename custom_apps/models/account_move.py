# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move.line"
    
    etiquet_analytic_id = fields.Many2one("account.analytic.tag",string="Etiquette", store=True)
    
    account_id_cle = fields.Many2one(related='etiquet_analytic_id.account_id',string="Numero Compte", store=True)
    
    
    
    


