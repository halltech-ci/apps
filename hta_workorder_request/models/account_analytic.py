# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    product_request = fields.One2many('product.request', 'analytic_account_id', copy=False, check_company=True)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    