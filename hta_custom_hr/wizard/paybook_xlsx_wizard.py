# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


month_list = [('1', 'January'),
              ('2', 'February'),
              ('3', 'March'),
              ('4', 'April'),
              ('5', 'May'),
              ('6', 'June'),
              ('7', 'July'),
              ('8', 'August'),
              ('9', 'September'),
              ('10', 'October'),
              ('11', 'November'),
              ('12', 'December')
             ]

class PaybookReportWizard(models.TransientModel):
    _name = 'paybook.xlsx.report'
    _description = "Paie Book Report Wizard"
    
    @api.model
    def get_default_month(self):
        month = str(fields.Date.today().month)
        return month
    
    #date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    #date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    slip_month = fields.Selection(selection=month_list, string='Period', default=lambda self:self.get_default_month())
    salary_structure = fields.Many2one('hr.payroll.structure', string="Structure du Salaire")
    employee = fields.Many2one('hr.employee', string="Employee")

    def print_xlsx(self):
        #I get data enter in form
        data = {
            'model': self._name,
            'ids' : self.ids,
            'month': self.slip_month[0],
            'structure_id': self.salary_structure[0],#.id,
            'employee': self.employee.id,
            #'model':'paybook.report.wizard',
            'form': self.read()[0]
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('hta_custom_hr.paybook_excel_report').with_context(landscape=True).report_action(self, data=data)

