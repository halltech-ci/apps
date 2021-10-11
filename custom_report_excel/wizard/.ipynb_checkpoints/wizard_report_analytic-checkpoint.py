# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import models, fields, api

class AccountAnalyticReportWizard(models.TransientModel):
    _inherit = 'account.analytic.report.wizard'
    
    def get_excel(self):
        data = {
            'date_start':self.date_start,
            'date_end':self.date_end,
            'analytic':self.analytic.ids,
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report_excel.account_analytic_report_xlsx').with_context(landscape=True).report_action(self, data=data)

