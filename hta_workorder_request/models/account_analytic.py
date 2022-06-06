# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    #product_request = fields.One2many('product.request', 'analytic_account_id', copy=False, check_company=True)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    product_line = fields.One2many('product.request.line', 'analytic_line', string="Product line")
    planned_date = fields.Date('Planned Date')
    
    def _timesheet_postprocess_values(self, values):
        res = super(AccountAnalyticLine, self)._timesheet_postprocess_values(values)
        # Delete the changes in amount if the analytic lines
        # come from product_line.
        for key in (self.filtered(lambda x: x.product_line).ids):
            res[key].pop('amount', None)
        return res
    