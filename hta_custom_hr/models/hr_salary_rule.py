# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HrSalaryRule(models.Model):
    _inherit ='hr.salary.rule'
    
    appears_on_paybook = fields.Boolean(string="On Paybook", default=True)
    
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    slip_month = fields.Char(string='Slip Month', store=True, compute='compute_slip_month')
    
    #check unique payslip for employee for a given date
    """@api.constrains('slip_month', 'employee_id')
    def _unique_slip_id_per_date(self):
        for record in self:
            res = self.env['hr.payslip'].search([('slip_month', '=', record.slip_month), ('employee_id', '=', record.employee_id.id)])
            if len(res) > 1:
                raise ValidationError("You cannot create duplicate payslip for employee {0}. Payslip already exist.".format(record.employee_id.name))"""
    
    @api.depends('date_from')
    def compute_slip_month(self):
        for slip in self:
            slip.slip_month = slip.date_from.month

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'
    
    appears_on_paybook = fields.Boolean(related='salary_rule_id.appears_on_paybook', readonly=True)
    slip_month = fields.Char(related="slip_id.slip_month", string='Slip Month')