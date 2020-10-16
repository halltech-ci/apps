# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProfitLossReport(models.AbstractModel):
    _name = "report.hta_custom_report.hta_profit_loss"
    
    
    def _get_lines(self, data):
        company = data['form']['company_id']
        start_date = data['form']['start_date']
        start_date = data['form']['end_date']
        target = start_date = data['form']['target_move']
    
    def _get_report_value(self):
        pass