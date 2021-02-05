# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class AccountCashReportWizard(models.TransientModel):
    _name = 'account.cash.report.wizard'
    _description = "Wizard Caisse"
    

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    #partner = fields.Many2one('hr.partner', string="Partner")
    cash_journal = fields.Many2one('account.bank.statement', string="Relevé", default=lambda self: self.get_default_cash_journal())

    def get_report(self):
        data = {
            'model':'account.cash.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report.account_cash_report').with_context(landscape=True).report_action(self, data=data)
    
    def get_default_cash_journal(self):
        import datetime
        date = datetime.date.today()
        month = date.month
        res = self.env['account.bank.statement'].search([]).filtered(lambda l:l.date.month==month)
        return res
        
