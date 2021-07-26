# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PaybookReport(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_custom_hr.paybook_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Paie Book Excel Report"
    
    def get_lines(self, month, rule_id, employee=None):
        domain = [('slip_month', '=', month), ('appears_on_paybook', '=', True), ('salary_rule_id', '=', rule_id)]
        
        if employee:
            domain.append(('employee_id', '=', employee))
        lines = self.env['hr.payslip.line'].search(domain)
        return lines
    
    
    def generate_xlsx_report(self, workbook, data, partners):
        month = data['form']['slip_month'][0]
        struct_id = data['form']['salary_structure'][0]
        employees = self.env['hr.payslip'].search([('slip_month', '=', month)]).employee_id#.ids
        salary_rule = self.env['hr.salary.rule'].search([('struct_id', '=', struct_id) ,('appears_on_paybook', '=', True)], order = 'rubrique asc')
        lines = self.get_lines
        
        bold = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#fffbed', 'border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
        worksheet.set_column('A:A', 40)
        
        for employee in employees:
            employee_name = employee.name
            # One sheet by partner
            sheet = workbook.add_worksheet(employee_name)
            bold = workbook.add_format({'bold': True})
            sheet.write(0, 0, employee.name, bold)
        
    