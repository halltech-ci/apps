# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'
    
    def action_view_reconcile(self):
        view_id = self.env['ir.ui.view'].search([('name', '=', 'account_statement_reconcile_tree')]).id
        return {
                'type': 'ir.actions.act_window',
                'name': 'Lettrage Caisse',
                'target': 'main', #use 'current' for not opening in a dialog
                'res_model': 'account.bank.statement.line',
                'domain': [('statement_id', '=', self.id)],
                'view_type': 'tree',
                'views': [[view_id,'tree']],
                };
    
class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"
    
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='set null')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags', 
        relation='account_statement_model_analytic_tag_rel'
    )
    
    def button_action_reconcile(self):
        pass 
    


    
