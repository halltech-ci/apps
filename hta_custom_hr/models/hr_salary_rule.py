# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrSalaryRule(models.Model):
    _inherit ='hr.salary.rule'
    
    appears_on_paybook = fields.Boolean(string="On Paybook", default=True)
    
class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'
    
    appears_on_paybook = fields.Boolean(related='salary_rule_id.appears_on_paybook', readonly=True)