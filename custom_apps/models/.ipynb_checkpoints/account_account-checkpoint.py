# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAccountTag(models.Model):
    _inherit = "account.account"
    
    account_tag = fields.Many2one("account.analytic.tag", "Etiquette", ondelete= "cascade",store=True)
    


