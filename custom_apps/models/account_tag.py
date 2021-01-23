# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAccountTag(models.Model):
    _inherit = "account.analytic.tag"
    
    account_id = fields.Many2one("account.account", "Account", ondelete= "cascade")
    


