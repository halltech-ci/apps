# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    
    product_request = fields.One2many('product.request', 'analytic_account_id', copy=False, check_company=True)

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    stock_task_id = fields.Many2one('project.task', string = 'Project Task')
    
    '''def _timesheet_postprocess_values(self, values):
        """When hr_timesheet addon is installed, in the create() and write() methods,
        the amount is recalculated according to the employee cost.
        We need to force that in the records related to stock tasks the price is not
        updated."""
        res = super()._timesheet_postprocess_values(values)
        for key in self.filtered(lambda x: x.stock_task_id).ids:
            res[key].pop("amount", None)
        return res
    '''