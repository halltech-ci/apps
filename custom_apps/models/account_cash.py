# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountCash(models.Model):
    _inherit = "account.bank.statement.line"
    
    project_id = fields.Many2one("project.project", "Project",store=True)
    


