# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'
    
    def button_cash_report(self):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Rapport de caisse',
                'target': 'new', #use 'current' for not opening in a dialog
                'res_model': 'account.cash.report.wizard',
                #'res_id': self.env['stock.request.order'].search([('project_task', '=', self.id)]).id,
                #'view_id': 'view_xml_id',#optional
                'view_type': 'form',
                'views': [[False,'form']],
                };