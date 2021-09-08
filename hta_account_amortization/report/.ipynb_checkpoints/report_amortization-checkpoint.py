from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportAccountAmortizationReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_account_amortization.account_amortization_report_view'
    
    _description = 'Report Account Amortization'
    

    
    def get_lines(self, amortization_id, date_start,date_end):
        
        params = [tuple(amortization_id),date_start,date_end]
        query = """
                SELECT aas.name AS designation, aas.acquisition_date AS date_acquisition, SUM(ass.original_value) AS valeur_acquisition, am.date AS date_exercice, SUM(aml.asset_remaining_value)-SUM(aml.asset_depreciation_value)) AS anterieur, SUM(am.amount_total) AS exercice,SUM(am.asset_depreciation_value) AS total, SUM(am.asset_remaining_value) AS valeur_residuelle
                FROM account_move AS am
                INNER JOIN account_asset AS aas ON aas.id = am.asset_id
                WHERE
                    (aas.id IN %s)
                    AND
                    (am.date BETWEEN %s AND %s)

                GROUP BY designation, date_acquisition,date_exercice
        """

        self.env.cr.execute(query,params)
        return self.env.cr.dictfetchall()
      
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)

        docs = []
        if data['form']['project']:
            project = data['form']['project'][0]
            lines = self.env['account.asset'].search([('id','=',project)])
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
            
        
        return {
            'doc_model': 'account.analytic.line',
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
    _name = 'report.hta_account_amortization.account_amortization_report_xlsx_generate'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Account Amortization XLM'
    
    def get_lines(self, amortization_id, date_start,date_end):
        
        params = [tuple(amortization_id),date_start,date_end]
        query = """
                SELECT aas.name AS designation, aas.acquisition_date AS date_acquisition, SUM(ass.original_value) AS valeur_acquisition, am.date AS date_exercice, SUM(aml.asset_remaining_value)-SUM(aml.asset_depreciation_value)) AS anterieur, SUM(am.amount_total) AS exercice,SUM(am.asset_depreciation_value) AS total, SUM(am.asset_remaining_value) AS valeur_residuelle
                FROM account_move AS am
                INNER JOIN account_asset AS aas ON aas.id = am.asset_id
                WHERE
                    (aas.id IN %s)
                    AND
                    (am.date BETWEEN %s AND %s)

                GROUP BY designation, date_acquisition,date_exercice
        """

        self.env.cr.execute(query,params)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
    
        sheet = workbook.add_worksheet('Account Report Result')
        bold = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#fffbed', 'border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border': True})

        sheet.merge_range('A1:F1', 'Report Result', title)
        
        
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)

        docs = []
        mylist = ["Vente de Marchandise", "Achat de Marchandise", "Variation de stocks de Marchandise",
                 "MARGE  COMMERCIALE", "Ventes de produits fabriqués", "Travaux, services vendus",
                 "Produits accessoires", "CHIFFRE D'AFFAIRES", "Production stockée (ou déstockage)",
                 "Production immobilisée", "Subventions d'exploitation", "Autres produits",
                 "Transferts de charges d'exploitation", "Achats de matières premières et fournitures liées", "Variation de stocks de matières premières et fournitures liées",
                 "Autres achats", "Variation de stocks d’autres approvisionnements", "Transports",
                 "Services extérieurs", "Impôts et taxes", "Autres charges",
                 "VALEUR AJOUTEE", "Charges de personnel", "EXCEDENT BRUT D'EXPLOITATION","Reprises d’amortissements, de provisions et dépréciations",
                 "Dotations aux amortissements, aux provisions et dépréciations", "RESULTAT D'EXPLOITATION", "Revenus financiers et assimilés",
                 "Reprises de provisions et dépréciations financières", "Transferts de charges financières", "Frais financiers et charges assimilés",
                 "Dotations aux provisions et aux dépréciations financières", "RESULTAT  FINANCIER", "RESULTAT  DES ACTIVITES ORDINAIRES",
                 "Produits des cessions d'immobilisations", "Autres Produits HAO", "Valeurs comptables des cessions d'immobilisations",
                 "Autres Charges HAO", "RESULTAT HORS ACTIVITES ORDINAIRES", "Participation des travailleurs",
                 "Impôts sur le résultat", "RESULTAT NET",]
        
        if data.get('project'):
            project = data.get('project')
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            account = line.analytic_account_id.id
            id_aan = str(account)
            
            get_lines = self.get_lines(id_aan,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
        
        row = 2
        col = 0
    
        # Header row
        
        sheet.write(row, col, 'Projet/Line')
        
        nombre = 0
        col +=1
        for line in docs:
            sheet.write(row, col+nombre, line['name'])
            nombre = nombre + 1
        
        row +=1
        col = 0
        i = 0
        for ligne in mylist:
            compte = 1
            for line in docs:
                sheet.write(row+i, col, ligne)
                sheet.write(row+i, col+compte, line['get_lines'][i][0])
                compte = compte + 1
            i +=1
                
        #bold = workbook.add_format({'bold': True})
        #sheet.write(0, 0, obj.name, bold)