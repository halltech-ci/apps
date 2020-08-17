# -*- coding: utf-8 -*-

from odoo import models, fields, api



class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    imported_from_timesheet = fields.Boolean(
        string='Imported From Timesheet',
        default=False
    )
    timesheet_sheet_id = fields.Many2one(
        string='Timesheet',
        comodel_name='hr_timesheet.sheet'
    )
