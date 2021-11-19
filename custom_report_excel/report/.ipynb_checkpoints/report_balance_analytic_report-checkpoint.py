import datetime,calendar

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportBalanceAnalyticReportExcel(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report_excel.balance_analytic_report_excel'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Balance Analytic XLM'
    


    def get_lines(self, analytic_id, date_start,date_end):
        
        params = [tuple(analytic_id),date_start,date_end]
        query = """
                SELECT x_aa.code AS code_account, x_aa.name AS name_account, pp.code AS code_project, pp.name AS name_project, x_aat.name AS name_analytic, SUM(x_aml.debit) AS x_debit, SUM(x_aml.credit) AS x_credit, (SUM(x_aml.debit)-SUM(x_aml.credit)) AS solde_debit, (SUM(x_aml.credit)-SUM(x_aml.debit)) AS solde_credit

                FROM account_move_line AS x_aml
                LEFT JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id
                LEFT JOIN account_analytic_tag AS x_aat ON  x_aat.id = x_aml.etiquet_analytic_id
                LEFT JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id
                LEFT JOIN project_project AS pp ON pp.analytic_account_id = x_aan.id
                WHERE 
                    ( x_aa.code LIKE '6%') OR ( x_aa.code LIKE '7%') OR ( x_aa.code LIKE '8%')
                    AND
                    (x_aml.analytic_account_id = """+ analytic_id+""")
                    AND
                    (x_aml.date BETWEEN '%s' AND '%s')
                GROUP BY code_project,name_project,name_analytic,code_account,name_account
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Balance Analytic Report ')
        
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
                {'align': 'center', 'font_size': 12})
        table_body_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_body_group_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 40)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 15)

        
        row = 2
        col = 0
        sheet.merge_range(row, col, row, col+8,  'Balance Analytique', title)

        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        docs = []
        if data.get('analytic'):
            analytic_id =data.get('analytic')
            lines = self.env['account.move.line'].search([('analytic_account_id','=',analytic_id),
                                                                 ('create_date','>=',date_start),
                                                                 ('create_date','<=',date_end)])
        else:
            lines = self.env['account.move.line'].search([('analytic_account_id','!=',False),
                                                          ('create_date','>=',date_start),
                                                         ('create_date','<=',date_end)])
        for line in lines:
            analytic = line.analytic_account_id.id
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
        sheet.merge_range(row, col, row+1, col, 'Numero Compte', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Libelle Compte', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'Code Projet', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'Description', table_header)
        sheet.merge_range(row, col+4, row+1, col+4, 'Section Analytic', table_header)
        sheet.merge_range(row, col+5, row+1, col+5, 'M. Debit', table_header)
        sheet.merge_range(row, col+6, row+1, col+6, 'M. Credit', table_header)
        sheet.merge_range(row, col+7, row+1, col+7, 'S. Debit', table_header)
        sheet.merge_range(row, col+8, row+1, col+8, 'S. Credit', table_header)
        
        ligne = 5
        j = 0
        i = 1
        for line in docs:
            for analytic in line['get_lines']:
                sheet.write(ligne+i, col, analytic.get('code_account'),table_body_space)
                sheet.write(ligne+i, col+1, analytic.get('name_account'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('code_project'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('name_project'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('name_analytic'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('x_debit'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('x_credit'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('solde_debit'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('solde_credit'),table_body_space)
                i +=1