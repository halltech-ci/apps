# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PaybookReport(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_custom_hr.paybook_template'
    _description = 'Report Paie Book'
    
    def get_lines(self, date_start, date_end, employee=None):
        params = [date_start, date_end]
        query = """
                SELECT * 
                FROM hr_payslip_line AS p_line
                WHERE
                p_line.date_from >= %s
                AND p_line.date_to <= %s
            """
        if employee:
            params.append(employee)
            employee_query =  ' AND p_line.employee_id = %s'
            query = """
                SELECT * 
                FROM hr_payslip_line AS p_line
                WHERE
                p_line.appears_on_paybook = True
                AND p_line.date_from >= %s
                AND p_line.date_to <= %s """ + employee_query + """
            """
        self.env.cr.execute(query, params)
        return self.env.cr.dictfetchall()
    
    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        struct_id = data['form']['salary_structure'][0]
        employee = self.env['hr.payslip.line'].search([('date_from', '>=', date_start), ('date_to', '<=', date_end)]).employee_id.ids
        salary_rule = self.env['hr.salary.rule'].search([('struct_id', '=', struct_id) ,('appears_on_paybook', '=', True)])
        lines = self.get_lines
        docs = []
        return {
            'doc_ids': data['ids'],
            'docs': docs,
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'lines' : lines,
            'employee_ids': employee,
            'salary_rule': salary_rule,
            #'employee': data['form']['employee'][0],
            
        }
        
        
            
        
    