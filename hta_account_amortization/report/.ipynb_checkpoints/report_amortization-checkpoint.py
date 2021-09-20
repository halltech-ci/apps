import datetime,calendar

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportAccountAmortizationReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_account_amortization.amortization_report_view'
    
    _description = 'Report Account Amortization'

    
    def get_lines(self, amortization_type, amortization_id, date_start,date_end):
        
        #params = [tuple(amortization_type),tuple(amortization_id),date_start,date_end]
        query = """
                SELECT haat.name AS group_designation,haat.number_percentage AS taux_group, aas.name AS designation, aas.acquisition_date AS date_acquisition, SUM(aas.original_value) AS valeur_acquisition, am.date AS date_exercice, (SUM(am.asset_depreciated_value)-SUM(am.amount_total)) AS anterieur, SUM(am.amount_total) AS exercice,SUM(am.asset_depreciated_value) AS total, SUM(am.asset_remaining_value) AS valeur_residuelle
                FROM account_move AS am
                INNER JOIN account_asset AS aas ON aas.id = am.asset_id
                INNER JOIN hta_account_asset_type AS haat ON haat.id = aas.type_asset_ids
                WHERE
                    (haat.id = """+ amortization_type+""")
                    AND
                    (aas.id = """+ amortization_id+""")
                    AND
                    
                    (am.date BETWEEN '%s' AND '%s')

                GROUP BY group_designation,taux_group, designation, date_acquisition,date_exercice
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
      
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        format_str = '%Y-%m-%d' # The format
        start_date = datetime.datetime.strptime(date_start, format_str).date()
        end_date = datetime.datetime.strptime(date_end, format_str).date()

        docs = []
        if data['form']['amortization_type']:
            amortization_type = data['form']['amortization_type'][0]
            lines = self.env['hta.account_asset.type'].search([('id','=',amortization_type)])
        else:
            lines = self.env['hta.account_asset.type'].search([])
        
        if data['form']['amortization']:
            amortization = data['form']['amortization'][0]
            lines_amortization = self.env['account.asset'].search([('id','=',amortization)])
        else:
            lines_amortization = self.env['account.asset'].search([])
            
        for line in lines:
            type = line.id
            id_type = str(type)
            for line_am in lines_amortization:
                amort = line_am.id
                id_amort = str(amort)
            
                get_lines = self.get_lines(id_type,id_amort,date_start,date_end)
                name = line_am.name
            
                docs.append ({
                    'name': name,
                    'get_lines':get_lines,
                })
        
        return {
            'doc_model': 'account.amortization.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }

class ReportAccountAmortizationReportXlsxGenerate(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_account_amortization.asset_xlsx_generate'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Account Amortization XLM'
    
    def get_lines(self, amortization_type, amortization_id, date_start,date_end):
        
        params = [tuple(amortization_type),tuple(amortization_id),date_start,date_end]
        query = """
                SELECT haat.name AS group_designation,haat.number_percentage AS taux_group, aas.name AS designation, aas.acquisition_date AS date_acquisition, SUM(aas.original_value) AS valeur_acquisition, am.date AS date_exercice, (SUM(am.asset_remaining_value)-SUM(am.asset_depreciated_value)) AS anterieur, SUM(am.amount_total) AS exercice,SUM(am.asset_depreciated_value) AS total, SUM(am.asset_remaining_value) AS valeur_residuelle
                FROM account_move AS am
                INNER JOIN account_asset AS aas ON aas.id = am.asset_id
                INNER JOIN hta_account_asset_type AS haat ON haat.id = aas.type_asset_ids
                WHERE
                    (haat.id IN %s)
                    AND
                    (aas.id IN %s)
                    AND
                    (am.date BETWEEN %s AND %s)

                GROUP BY group_designation,taux_group, designation, date_acquisition,date_exercice
        """

        self.env.cr.execute(query,params)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Account Report Amortization')
        
        company_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black','bold': True,})
        title = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 21,
                    'font_color': 'black', 'bold': True, 'border': 1})
        table_header = workbook.add_format(
                {'bg_color': '#8f8e8d', 'align': 'center', 'font_size': 14,
                    'font_color': 'black'})
        table_body_space = workbook.add_format(
                {'align': 'left', 'font_size': 12, 'border': 1})
        table_body_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_body_group_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        sheet.set_column('A:A', 50)
        
        row = 2
        col = 0
        sheet.merge_range(row, col, row, col+1,  'Raison sociale: CONCEPTOR INDUSTRY', company_format)
        sheet.merge_range(row+1, col, row+1, col+1, 'N°CC : 1205248 Z', company_format)
        sheet.merge_range(row+2, col, row+2, col+7, 'TABLEAU D AMORTISSEMENTS ET INVENTAIRE DES IMMOBILISATIONS', title)
        
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        
        docs = []
        if data.get('amortization'):
            data.get('amortization')
            lines = self.env['account.asset'].search([('id','=',amortization)])
        else:
            lines = self.env['account.asset'].search([])
        for line in lines:
            account = line.id
            id_aas = str(account)
            
            get_lines = self.get_lines(id_aas,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
        row += 4
        col = 0
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        
        sheet.merge_range(row, col, row+1, col, 'DESIGNATION', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'TAUX', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'DATE ACQUISITION', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'VALEUR D ACQUISITION', table_header)
        sheet.merge_range(row, 4, row, 6, 'AMORTISSEMENT', table_header)
        sheet.write(row+1, 4, 'ANTERIEUR', table_header)
        sheet.write(row+1, 5, 'EXERCICE', table_header)
        sheet.write(row+1, 6, 'TOTAL', table_header)
        sheet.merge_range(row, col+7, row+1, col+7, 'VALEUR RESIDUELLE', table_header)
        # Header row
        
        