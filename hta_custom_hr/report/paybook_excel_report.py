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
        month = data['form']['slip_month']#[0]
        struct_id = data['form']['salary_structure'][0]
        employees = self.env['hr.payslip'].search([('slip_month', '=', month), ('state', 'in', ('done', 'verify'))]).employee_id#.ids
        rules = self.env['hr.salary.rule'].search([('struct_id', '=', struct_id) ,('appears_on_paybook', '=', True)], order = 'rubrique asc')
        
        bold_bg = workbook.add_format({'bold': True, 'align': 'left', 'bg_color': '#fffbed', 'border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
        left_row_style = workbook.add_format({'bold': False, 'align': 'left', 'border': True})
        cel_row_style = workbook.add_format({'bold': False, 'align': 'center', 'border': True})
        cel_row = workbook.add_format({'bold': False, 'align': 'left', 'border': True})
        cel_row_style_bg = workbook.add_format({'bold': True, 'align': 'center', 'border': True, 'bg_color': '#fffbed'})
        bold_row_style = workbook.add_format({'bold': True, 'align': 'left', 'border': True, 'bg_color': '#fffbed'})
        bold_row = ['TCOTEM', 'SBI']
        col = 1
        row = 3
        sheet = 'Livre de Paie' + '-' + month
        worksheet = workbook.add_worksheet("Livre de paie")
        worksheet.write(row, 0, "Noms et Prénoms", bold_bg)
        worksheet.set_column(0, 0, 30)
        for rule in rules:
            TOTAL = 0
            worksheet.set_column(row, col, 30)
            worksheet.write_string(row, col, rule.name, bold_bg)
            row_1 = row + 1
            for employee in employees:
                worksheet.write_string(row_1, 0, employee.name, cel_row)
                line = self.get_lines(month, rule.id, employee.id)#[0]
                worksheet.write_number(row_1, col, line.amount, cel_row_style)
                TOTAL += line.amount
                row_1 += 1
            worksheet.write_string(row_1, 0, "TOTAL", header_row_style)
            worksheet.write_number(row_1, col, TOTAL, header_row_style)
            col += 1    
        
    