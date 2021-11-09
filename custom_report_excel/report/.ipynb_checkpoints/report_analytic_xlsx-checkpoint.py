import datetime,calendar

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportAccountAnalyticReportXlsxGenerate(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report_excel.analytic_report_excel'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Account Analytic XLM'
    


    def get_lines(self, analytic_id, date_start,date_end):
        
        params = [tuple(analytic_id),date_start,date_end]
        query = """
                SELECT x_aan.name AS x_analytic_account_id, SUM(x_aml.debit) AS x_debit, SUM(x_aml.credit) AS x_credit, (SUM(x_aml.credit)-SUM(x_aml.debit)) AS resultat
                FROM account_move_line AS x_aml
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id

                WHERE 
                    (( x_aa.code LIKE '6%'
                                OR x_aa.code LIKE '81%'
                                OR x_aa.code LIKE '83%'
                                OR x_aa.code LIKE '85%'
                                OR x_aa.code LIKE '87%'
                                OR x_aa.code LIKE '89%'

                            ) OR ( x_aa.code LIKE '7%'
                                OR x_aa.code LIKE '82%'
                                OR x_aa.code LIKE '84%'
                                OR x_aa.code LIKE '86%'
                                OR x_aa.code LIKE '88%'


                            ))
                            AND
                            (x_aml.analytic_account_id = """+ analytic_id+""")
                            AND
                            (x_aml.date BETWEEN '%s' AND '%s')
                GROUP BY x_analytic_account_id
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Account Analytic Report ')
        
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
        sheet.set_column('D:D', 30)

        
        row = 2
        col = 0
        sheet.merge_range(row, col, row, col+3,  'Rapport Analytique', title)

        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        docs = []
        
        if data.get('analytic'):
            analytic_id = data.get('analytic')
            lines = self.env['account.analytic.account'].search([('id','=',analytic_id)])
        else:
            lines = self.env['account.analytic.account'].search([])
        for line in lines:
            analytic = line.id
            id_aan = str(analytic)
            
            get_lines = self.get_lines(id_aan,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
        
        row += 2
        col = 0
        
        # Header row
        sheet.merge_range(row, col, row+1, col, 'Analytic Account', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Charge', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'Produit', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'Resultat', table_header)
        
        ligne = 5
        j = 0
        i = 1
        for line in docs:
            for analytic in line['get_lines']:
                sheet.write(ligne+i, col, analytic.get('x_analytic_account_id'))
                sheet.write(ligne+i, col+1, analytic.get('x_debit'))
                sheet.write(ligne+i, col+2, analytic.get('x_credit'))
                sheet.write(ligne+i, col+2, analytic.get('resultat'))
                i +=1
        
        
   

           
        