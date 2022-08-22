# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    is_done = fields.Boolean(default=False)