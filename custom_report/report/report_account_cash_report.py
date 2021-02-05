from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportCashReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.cash_report_view'
    
    _description = 'Report Account Cash'
    def get_amount_montant_init(self, statement_id, balance_final,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (x_absl.date) AS x_date, SUM(x_absl.amount) AS x_amount_depense, SUM("""+str(balance_final)+""") AS x_balance, (("""+str(balance_final)+""")-SUM(x_absl.amount)) AS x_montant_init
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        GROUP BY x_date
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    def get_amount_depense(self, statement_id, balance_final,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (x_absl.date) AS x_date, SUM(x_absl.amount) AS x_amount_depense, SUM("""+str(balance_final)+""") AS x_balance
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.amount < 0)
                            AND
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        GROUP BY x_date
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    def get_amount_appro(self, statement_id, balance_final,date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (x_absl.date) AS x_date, SUM(x_absl.amount) AS x_amount_profil,SUM("""+str(balance_final)+""") AS x_balance
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        WHERE
                            (x_absl.amount > 0)
                            AND
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        GROUP BY x_date
                        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    
    def get_lines(self, statement_id,balance_final, date_start,date_end):
        
        #params = [balance_final,tuple(statement_id),date_start,date_end]
        query = """
                        SELECT (x_absl.date) AS x_date, x_absl.ref AS x_reference, x_absl.name AS x_libelle, x_pp.name AS x_project, x_absl.partner_id x_partner, x_absl.amount AS x_amount, SUM("""+str(balance_final)+""") AS x_balance,(("""+str(balance_final)+""")-SUM(x_absl.amount)) AS x_montant_initial, SUM(x_absl.amount) AS x_sum_amount
                        FROM account_bank_statement_line AS x_absl
                        INNER JOIN account_bank_statement AS x_abs ON x_abs.id = x_absl.statement_id
                        LEFT JOIN project_project AS x_pp ON x_pp.id = x_absl.project_id
                        WHERE   
                            (x_absl.statement_id = """+str(statement_id)+""")
                             AND
                            (x_absl.date BETWEEN '%s' AND '%s')
                        GROUP BY x_date,x_reference, x_libelle, x_project, x_partner,x_amount
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
                montant_init = bank_line.amount
                date_statement = str(date_lines)
                libelle = bank_line.name
                partner = bank_line.partner_id
                montant = bank_line.amount
                
                balance_final = amount + balance_start   
                montant_initial = balance_final - (amount)  
            name_lines = bank_line.name
            balance_days = amount + balance_start
            get_lines = self.get_lines(statement_id,balance_final,
                                               date_start,date_end)
            
            get_amount_appro = self.get_amount_appro(statement_id,balance_final,
                                               date_start,date_end)
            get_amount_depense = self.get_amount_depense(statement_id,balance_final,
                                               date_start,date_end)
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
            'montant_sum':montant_init,
            'montant_initial':montant_initial,
            'balance_final_days':balance_final,
            'amount':amount,
            'cash': cash,
            'get_lines':self.get_lines,
        }