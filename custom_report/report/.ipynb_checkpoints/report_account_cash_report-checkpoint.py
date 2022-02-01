from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportCashReportView(models.AbstractModel):
    """
        Abstract Model specially for report templates.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.cash_report_view'
    
    _description = 'Report Account Cash'
    
    # Recuperer le montant initial de la caisse à une date donnée
    def get_amount_montant_init(self, statement_id, balance_final,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (("""+str(balance_final)+""")-SUM(x_absl.amount)) AS x_montant_init
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    # requette sql pour Recuperer les depenses de la caisse à une date donnée
    def get_amount_depense(self, statement_id,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT SUM(x_absl.amount) AS x_amount_depense
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.amount < 0)
                            AND
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    # requette sql pour Recuperer les appro de la caisse à une date donnée
    def get_amount_appro(self, statement_id,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT SUM(x_absl.amount) AS x_amount_profil
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.amount > 0)
                            AND
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                       
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    # requette sql pour Recuperer les lignes des transaction de la caisse à une date donnée
    def get_lines(self, statement_id,balance_final, date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (x_absl.date) AS x_date, x_absl.ref AS x_reference, x_absl.name AS x_libelle, x_pp.name AS x_project, x_rp.name x_partner, x_absl.amount AS x_amount, SUM("""+str(balance_final)+""") AS x_balance,(("""+str(balance_final)+""")-SUM(x_absl.amount)) AS x_montant_initial, SUM(x_absl.amount) AS x_sum_amount
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        LEFT JOIN project_project AS x_pp ON x_pp.id = x_absl.project_id
                        LEFT JOIN res_partner AS x_rp ON x_rp.id = x_absl.partner_id
                        WHERE   
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        GROUP BY x_date,x_reference, x_libelle, x_project, x_partner,x_amount
                        ORDER BY x_date ASC
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
      

    @api.model
    def _get_report_values(self, docids, data=None):
        import datetime

        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        
        bank_statement_line = self.env['account.bank.statement.line']
        
        docs = []
        cash = []
        
        if data['form']['cash_journal']:
            bank_statement_id = data['form']['cash_journal'][0]
            lines = self.env['account.bank.statement'].search([('id','=',bank_statement_id)])
        else:
            lines = self.env['account.bank.statement'].search([])
            
        date_time_str = date_start
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
        for line in lines:
            date = line.date
            balance_start = line.balance_start
            statement_id = line.id
            name = line.name
            amount = 0
            depense = 0
            balance_final = 0
            for bank_line in bank_statement_line.search([('statement_id','=',statement_id),
                                                         ('date','>=',date),
                                                         ('date','<=',date_end)]):
                date_lines = bank_line.date
                amount = bank_line.amount + amount
                date_lines = bank_line.date
               
                date_statement = str(date_lines)
                libelle = bank_line.name
                partner = bank_line.partner_id
                montant = bank_line.amount
                
                balance_final = amount + balance_start   
            name_lines = line.name
            
            get_lines = self.get_lines(statement_id,balance_final,
                                               date_start,date_end)
            get_amount_appro = self.get_amount_appro(statement_id,date_start,date_end)
            
            get_amount_depense = self.get_amount_depense(statement_id,date_start,date_end)
            
            get_amount_montant_init = self.get_amount_montant_init(statement_id,balance_final,
                                               date_start,date_end)

            docs.append ({
                    'name': name_lines,
                    'get_lines':get_lines,
                    'get_amount_appro':get_amount_appro,
                    'get_amount_depense':get_amount_depense,
                    'get_amount_montant_init':get_amount_montant_init,
                        
                    })
        
        return {
            'doc_model': 'account.analytic.report.wizard',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'balance_final_days':balance_final,
            'amount':amount,
            'cash': cash,
            'get_lines':self.get_lines,
        }

    

class ReportAccountCashReportXlsxGenerate(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.account_cash_xlsx_generate'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Account Cash XLM'
    

    
    # Recuperer le montant initial de la caisse à une date donnée
    def get_amount_montant_init(self, statement_id, balance_final,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (("""+str(balance_final)+""")-SUM(x_absl.amount)) AS x_montant_init
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    # requette sql pour Recuperer les depenses de la caisse à une date donnée
    def get_amount_depense(self, statement_id,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT SUM(x_absl.amount) AS x_amount_depense
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.amount < 0)
                            AND
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    # requette sql pour Recuperer les appro de la caisse à une date donnée
    def get_amount_appro(self, statement_id,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT SUM(x_absl.amount) AS x_amount_profil
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.amount > 0)
                            AND
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                       
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    # requette sql pour Recuperer les lignes des transaction de la caisse à une date donnée
    def get_lines(self, statement_id,balance_final, date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (x_absl.date) AS x_date, x_absl.ref AS x_reference, x_absl.name AS x_libelle, x_pp.name AS x_project, x_rp.name x_partner, x_absl.amount AS x_amount, SUM("""+str(balance_final)+""") AS x_balance,(("""+str(balance_final)+""")-SUM(x_absl.amount)) AS x_montant_initial, SUM(x_absl.amount) AS x_sum_amount
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        LEFT JOIN project_project AS x_pp ON x_pp.id = x_absl.project_id
                        LEFT JOIN res_partner AS x_rp ON x_rp.id = x_absl.partner_id
                        WHERE   
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        GROUP BY x_date,x_reference, x_libelle, x_project, x_partner,x_amount
                        ORDER BY x_date ASC
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Account Report Cash')
        
        company_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black','bold': True,})
        title = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 28,
                    'font_color': 'black', 'bold': True, 'border': 1})
        
        montant_initial = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 16,
                    'font_color': 'black','bold': True,})
        
        table_header = workbook.add_format(
                {'bg_color': 'black', 'align': 'center', 'font_size': 18,
                    'font_color': 'white'})
        table_body_space = workbook.add_format(
                {'align': 'left', 'font_size': 12, 'border': 1})
        table_body_line = workbook.add_format(
                {'bg_color': '#eee8e2', 'align': 'center', 'font_size': 15,
                    'font_color': 'black', 'border': 1})
        table_body_group_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        table_recap = workbook.add_format(
                {'bg_color': '#f05987', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_recap_solde = workbook.add_format(
                {'bg_color': '#98ec6e', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        
        
        
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        docs = []
        bank_statement_line = self.env['account.bank.statement.line']
        
        if data.get('cash_journal'):
            bank_statement_id = data.get('cash_journal')
            lines = self.env['account.bank.statement'].search([('id','=',bank_statement_id)])
        else:
            lines = self.env['account.bank.statement'].search([])
            
        for line in lines:
            date = line.date
            balance_start = line.balance_start
            statement_id = line.id
            name = line.name
            amount = 0
            depense = 0
            balance_final = 0
            for bank_line in bank_statement_line.search([('statement_id','=',statement_id),
                                                         ('date','>=',date),
                                                         ('date','<=',date_end)]):
                date_lines = bank_line.date
                amount = bank_line.amount + amount
                date_lines = bank_line.date
               
                date_statement = str(date_lines)
                libelle = bank_line.name
                partner = bank_line.partner_id
                montant = bank_line.amount
                
                balance_final = amount + balance_start   
            name_lines = line.name
            
            get_lines = self.get_lines(statement_id,balance_final,
                                               date_start,date_end)
            get_amount_appro = self.get_amount_appro(statement_id,date_start,date_end)
            
            get_amount_depense = self.get_amount_depense(statement_id,date_start,date_end)
            
            get_amount_montant_init = self.get_amount_montant_init(statement_id,balance_final,
                                               date_start,date_end)
            
            docs.append ({
                    'name': name_lines,
                    'get_lines':get_lines,
                    'get_amount_appro':get_amount_appro,
                    'get_amount_depense':get_amount_depense,
                    'get_amount_montant_init':get_amount_montant_init,
                        
                    })
            
        sheet.set_column('A:A', 20)
        
        row = 2
        col = 0
        
        sheet.merge_range(row, col, row+1, col+5, 'RAPPORT CAISSE', title)
            
        row += 5
        col = 0
        sheet.set_column('B:B', 40)
        sheet.set_column('C:C', 50)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 20)
        
        
        
        sheet.merge_range(row, col, row+1, col, 'Date', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Libelle', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'Projet', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'Reference', table_header)
        sheet.merge_range(row, col+4, row+1, col+4, 'Partenaire', table_header)
        sheet.merge_range(row, col+5, row+1, col+5, 'Montant', table_header)
        # Header row
        
        
        
        ligne = 10
        i = 0
        for line in docs:
            for cash in line['get_lines']:
                sheet.write(ligne+i, col, cash.get('x_date').strftime('%d/%m/%Y'))
                sheet.write(ligne+i, col+1, cash.get('x_libelle'))
                sheet.write(ligne+i, col+2, cash.get('x_project'))
                sheet.write(ligne+i, col+3, cash.get('x_reference'))
                sheet.write(ligne+i, col+4, cash.get('x_partner'))
                sheet.write(ligne+i, col+5, cash.get('x_amount'))
                i +=1
