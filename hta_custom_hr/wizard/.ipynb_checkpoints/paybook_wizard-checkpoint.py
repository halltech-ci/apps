# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PaybookReportWizard(models.TransientModel):
    _name = 'paybook.report.wizard'
    _description = "Paie Book Report Wizard"
    

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    id_employee = fields.Many2one('hr.employee', string="Employee")

    def get_report(self):
        #I get data enter in form
        data = {
            'model':'paybook.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_custom_report.paybook_report').with_context(landscape=True).report_action(self, data=data)
