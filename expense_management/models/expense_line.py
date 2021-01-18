# -*- coding: utf-8 -*-

from odoo import models, fields, api

PAYMENT_MODE = [('justify', 'Employee (To justify)'),
                ('company', 'Company (Not justify)'),
                ('reimburse', 'Employee (To Reimburse)'),
               ]

PAYMENT_TYPE = [('cash', 'Espece'),
                ('trasfert', 'Mobile'),
                ('check', 'Cheque'),
               ]

REQUEST_STATE = [('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('to_approve', 'To Approve'),
        ('approve', 'Approved'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
        ]

class ExpenseLine(models.Model):
    _name = 'expense.line'
    _description = 'Custom expense line'
    
    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id
    
    @api.model
    def _get_employee_id_domain(self):
        employee_ids = self.env['hr.employee'].search([]).ids
        res = [('address_home_id.property_account_payable_id', '!=', False), ('id', 'in', employee_ids)]
        
        return res
    
    
    name = fields.Char('Description', required=True)
    request_state = fields.Selection(selection=REQUEST_STATE, string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    employee_id = fields.Many2one('hr.employee', string="Beneficiaire", required=True, check_company=True, domain=lambda self: self._get_employee_id_domain())
    request_id = fields.Many2one('expense.request', string='Expense Request')
    date = fields.Datetime(readonly=True, related='request_id.date', string="Date")
    amount = fields.Float("Montant", required=True, digits='Product Price')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, 
                                 default=lambda self: self.env.company
                                )
    requested_by = fields.Many2one('res.users' ,'Demandeur', track_visibility='onchange', related='request_id.requested_by')
    payment_mode = fields.Selection(selection=PAYMENT_MODE, string="Payment Mode", default='justify')
    payed_by = fields.Selection(selection=PAYMENT_TYPE, string="Payer Par", default='cash')
    analytic_account = fields.Many2one('account.analytic.account', string='Analytic Account')
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, 
                                  default=lambda self: self.env.company.currency_id
                                 )
    accounting_date = fields.Date(string='Accounting Date')
    debit_account = fields.Many2one('account.account', string='Debit Account')
    credit_account = fields.Many2one('account.account', string='Credit Account')
    transfer_amount = fields.Float('Frais de transfert', digits='Product Price')
    
    def action_submit(self):
        self._action_submit()

    def _action_submit(self):
        self.request_state = "submit"
        
    def action_to_approve(self):
        self.request_state = "to_approve"
    
    def action_approve(self):
        self.request_state = "approve"  
    
    def action_post(self):
        self.request_state = "post"
    def do_cancel(self):
        """Actions to perform when cancelling a purchase request line."""
        self.write({"request_state": 'cancel'})
    
    def _get_account_move_line_values(self):
        move_line_values_by_expense = {}
        for expense in self:
            move_line_name = expense.name
            account_src = expense.account_src
            account_dst = expense.account_dst
            account_date = fields.Date.context_today(expense)
            company_currency = expense.company_id.currency_id
            partner_id = expense.employee_id.address_home_id.commercial_partner_id.id
            move_line_values = []
            move_line_src = {
                'name': move_line_name,
                'debit': expense.amount if expense.amount > 0 else 0,
                'credit': -expense.amount if expense.amount < 0 else 0,
                'account_id': account_src.id,
                'analytic_account_id': expense.analytic_account.id,
                'expense_line_id': expense.id,
                'partner_id': partner_id,
                'currency_id': company_currency,
                }
            move_line_values.append(move_line_src)
            move_line_dst = {
                'name': move_line_name,
                'debit': amount > 0 and amount,
                'credit': total_amount < 0 and -amount,
                'account_id': account_dst,
                'date_maturity': account_date,
                'currency_id': company_currency,
                'expense_line_id': expense.id,
                'partner_id': partner_id,
            }
            move_line_values.append(move_line_dst)
            move_line_values_by_expense[expense.id] = move_line_values
        return move_line_values_by_expense
    
    def unlink(self):
        for expense in self:
            if expense.request_state in ['done', 'approved']:
                raise UserError(_('You cannot delete a posted or approved expense.'))
        return super(ExpenseLine, self).unlink()

    def write(self, vals):
        for expense in self:
            if expense.request_state in ['done', 'approved']:
                raise UserError(_('You cannot modify a posted or approved expense.'))
        return super(ExpenseLine, self).write(vals)
    
