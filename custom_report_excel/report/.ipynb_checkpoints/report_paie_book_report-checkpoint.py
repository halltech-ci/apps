import datetime,calendar

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class ReportPaieBookExcel(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report_excel.report_paie_book_excel'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Paie Book XLM'
    
    def get_line(self, date_start, date_end, employee=None,):
        params = [date_start, date_end]
        query = """
                SELECT * 
                FROM hr_payslip_line AS p_line
                WHERE
                (line.date_from >= %s)
                AND (line.date_to <= %)
            """
        if employee:
            params.append([tuple(employee)])
            employee_query =  ' AND (line.employee_id = %s)'
            query = """
                SELECT * 
                FROM hr_payslip_line AS p_line
                WHERE
                (line.date_from >= %s)
                AND (line.date_to <= %) """ + employee_query + """
            """
        self.env.cr.execute(query, params)
        return self.env.cr.dictfetchall()
    
    def get_lines(self, employee, date_start,date_end):

        params = [employee,date_start,date_end]
        query = """
            SELECT hpl.name AS x_hpl_name, hpl.code AS x_hpl_code, SUM(hpl.total) AS x_hpl_total, hpl.employee_id AS x_employee
            FROM hr_payslip AS hp
            INNER JOIN hr_contract AS x_hc ON hp.contract_id = x_hc.id
            INNER JOIN hr_payslip_line AS hpl ON hpl.slip_id = hp.id
            WHERE(
                (hpl.employee_id = %s)
                AND
                (hp.date_from BETWEEN %s AND %s)
                )
            GROUP BY x_hpl_name,x_hpl_code, x_employee
            """
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Livre de Paie')
        
        company_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black','bold': True,})
        title = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 21,
                    'font_color': 'black', 'bold': True, 'border': 1})
        table_header = workbook.add_format(
                {'bg_color': '#8f8e8d', 'align': 'center', 'font_size': 11,
                    'font_color': 'black','bold': True,})
        table_body_space = workbook.add_format(
                {'align': 'left', 'font_size': 12, 'border': 1})
        table_body_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_body_group_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        sheet.set_column('A:A', 40)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 40)

        
        row = 2
        col = 0
        sheet.merge_range(row, col, row, col+3,  'Livre de Paie', title)

        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        docs = []
        
        if data.get('id_employee'):
            employee = data.get('id_employee')
            lines_contrat = self.env['hr.contract'].search([('employee_id','=',employee)])
        else:
            lines_contrat = self.env['hr.contract'].search([])
        docs = []    
        for line in lines_contrat:
            if len(line.employee_id.slip_ids)>0:
                employee = line.employee_id.id
                employee_name = line.employee_id.name
                id_he = str(employee)
                get_lines = self.get_lines(id_he,date_start,date_end)
            
                docs.append({
                    'name':employee_name,
                    'get_lines':get_lines,
                })
        
        row += 2
        col = 0
        
        # Header row
        sheet.merge_range(row, col, row+1, col, 'Name', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Code', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'Total', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'Employé', table_header)
        
        ligne = 5
        j = 0
        i = 1
        for line in docs:
            for id_employee in line['get_lines']:
                sheet.write(ligne+i, col, analytic.get('x_hpl_name'))
                sheet.write(ligne+i, col+1, analytic.get('x_hpl_code'))
                sheet.write(ligne+i, col+2, analytic.get('x_hpl_total'))
                sheet.write(ligne+i, col+2, analytic.get('x_employee'))
                i +=1
        