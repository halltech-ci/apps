# -*- coding: utf-8 -*-

from odoo import models, fields, api

import time

class AccountAmortizationcReportWizard(models.TransientModel):
    _name = 'account.amortization.report.wizard'
    _description = "Wizard Amortization"
    

    date_start = fields.Date(string='Start Date', required=True,default=time.strftime('%Y-01-01'))
    date_end = fields.Date(string='End Date', required=True,default=time.strftime('%Y-12-31'))
    amortization = fields.Many2one('account.asset', string="Account Amortization")

    def get_report(self):
        data = {
            'model':'account.amortization.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_account_amortization.account_amortization_report').with_context(landscape=True).report_action(self, data=data)

    
    def get_generate_xlsx_report(self):
        data = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'amortization': self.amortization.ids, 
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_account_amortization.account_result_generate_xlsx_report').report_action(self, data=data)
