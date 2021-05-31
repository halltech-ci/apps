# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PaybookReport(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_custom_hr.paybook_template'
    _description = 'Report Paie Book'
    
    def get_lines(self, month, rule_id, employee=None):
        domain = [('slip_month', '=', month), ('appears_on_paybook', '=', True), ('salary_rule_id', '=', rule_id)]
        
        if employee:
            domain.append(('employee_id', '=', employee))
        lines = self.env['hr.payslip.line'].search(domain)
        return lines
    
    @api.model
    def _get_report_values(self, docids, data=None):
        month = data['form']['slip_month'][0]
        struct_id = data['form']['salary_structure'][0]
        employee = self.env['hr.payslip.line'].search([('slip_month', '=', month)]).employee_id#.ids
        salary_rule = self.env['hr.salary.rule'].search([('struct_id', '=', struct_id) ,('appears_on_paybook', '=', True)])
        lines = self.get_lines
        docs = []
        return {
            'doc_ids': data['ids'],
            'docs': docs,
            'doc_model': data['model'],
            #'date_start': date_start,
            #'date_end': date_end,
            'slip_month': month,
            'lines' : lines,
            'employee_ids': employee,
            'salary_rule': salary_rule,
            
        }
        
        
            
        
    