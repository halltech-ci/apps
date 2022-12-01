# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime

class HrPayslip(models.Model):
    _inherit = "hr.payslip"
    
    def _get_contract_wage(self):
        self.ensure_one()
        return self.contract_id.salaire_base
    
    slip_month = fields.Char(string='Slip Month', store=True, compute='compute_slip_month')
    worked_hours = fields.Float(string="Worked Hours", compute="_compute_worked_hours")
    
    @api.depends('date_from', 'date_to')
    def _compute_worked_hours(self):
        for slip in self:
            slip.worked_hours = slip.contract_id._get_work_hours(slip.date_from, slip.date_to)[1]
            
            
    def compute_sheet(self):
        for payslip in self.filtered(lambda slip: slip.state not in ['cancel', 'done']):
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            for employee in payslip.mapped('employee_id'):
                employee.compute_seniority()
            # delete old payslip lines
            payslip.line_ids.unlink()
            lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
            payslip.write({'line_ids': lines, 'number': number, 'state': 'verify', 'compute_date': fields.Date.today()})
        return True
    
    #check unique payslip for employee for a given date
    """@api.constrains('slip_month', 'employee_id')
    def _unique_slip_id_per_date(self):
        for record in self:
            res = self.env['hr.payslip'].search([('slip_month', '=', record.slip_month), ('employee_id', '=', record.employee_id.id), ])
            if len(res) > 1:
                raise ValidationError("You cannot create duplicate payslip for employee {0}. Payslip already exist.".format(record.employee_id.name))
    """
    
    @api.depends('date_from')
    def compute_slip_month(self):
        for slip in self:
            slip.slip_month = slip.date_from.month

class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'
    
    appears_on_paybook = fields.Boolean(related='salary_rule_id.appears_on_paybook', readonly=False)
    slip_month = fields.Char(related="slip_id.slip_month", string='Slip Month')