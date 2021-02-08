# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'
    
    def button_report_cash(self):
        pass