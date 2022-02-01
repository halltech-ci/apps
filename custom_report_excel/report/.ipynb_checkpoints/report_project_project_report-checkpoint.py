import datetime,calendar

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportProject(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report_excel.report_project_report_excel'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Project XLM'
    


    def get_lines(self, analytic_id, date_start,date_end):
        
        params = [tuple(analytic_id),date_start,date_end]
        query = """
                SELECT pp.name AS project, SUM(aml.debit) AS debit, SUM(aml.credit) AS credit, (SUM(aml.debit)-SUM(aml.credit)) AS marge
                FROM account_move_line AS aml
                INNER JOIN account_analytic_account AS aan ON aan.id = aml.analytic_account_id
                INNER JOIN project_project AS pp ON pp.analytic_account_id = aml.analytic_account_id
                INNER JOIN account_move AS am ON am.id = aml.move_id
                WHERE
                    (aml.analytic_account_id IN %s)
                    AND
                    (aml.date BETWEEN %s AND %s)

                GROUP BY project
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Report Project')
        
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
        
        sheet.set_column('A:A', 50)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 35)

        
        row = 2
        col = 0
        sheet.merge_range(row, col, row, col+3,  'Project Rapport', title)

        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        docs = []
        if data.get('project'):
            project = data.get('project')
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            project = line.analytic_account_id.id
            id_aan = str(project)
            
            
        row += 2
        col = 0
        
        # Header row
        sheet.merge_range(row, col, row+1, col, 'Project', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Chiffre Affaire', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'Coût', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'Marge', table_header)
        
        ligne = 5
        j = 0
        i = 1
        for line in docs:
            for project in line['get_lines']:
                sheet.write(ligne+i, col, analytic.get('project'))
                sheet.write(ligne+i, col+1, analytic.get('debit'))
                sheet.write(ligne+i, col+2, analytic.get('credit'))
                sheet.write(ligne+i, col+2, analytic.get('marge'))
                i +=1
        