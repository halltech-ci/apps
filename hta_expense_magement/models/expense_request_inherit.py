#-*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _

from odoo.exceptions import AccessError, UserError, ValidationError


class hta_expense_magement(models.Model):
    _inherit = 'expense.request'
    
    READONLY_STATES = {
        'to_cancel': [('readonly', True)],
        }
    name = fields.Char('Description', required=True)
    expense_approver = fields.Many2one('res.users', string="Valideur",states=READONLY_STATES)
    journal = fields.Many2one('account.journal', string='Journal', required=True, domain=[('type', 'in', ['cash', 'bank'])], states=READONLY_STATES, default=lambda self: self.env['account.journal'].search([('type', '=', 'cash')], limit=1))
    statement_id = fields.Many2one('account.bank.statement', string="Caisse",states=READONLY_STATES, tracking=True,default=lambda self: self.get_default_cash_journal())
    state = fields.Selection(selection_add=[('to_cancel', 'Annuler')], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', help='Expense Report State')

    line_ids = fields.One2many('expense.line', 'request_id', string='Expense Line',states={'to_cancel': [('readonly', True)]})
    
    def unlink(self):
        for expense in self:
            if not expense.state == 'to_cancel':
                raise UserError(_('In order to delete a expense request, you must cancel it first.'))
        return super(hta_expense_magement, self).unlink()
    
    
    def button_to_cancel(self):
        #self.is_approver_check()
        #self.mapped("line_ids").do_cancel()
        
        return self.write({'state': 'to_cancel'})
    
    def get_default_cash_journal(self):
        import datetime
        date = datetime.date.today()
        month = date.month
        res = self.env['account.bank.statement'].search([]).filtered(lambda l:l.date.month==month)
        return res

