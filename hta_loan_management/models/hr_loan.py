# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LoanRequest(models.Model):
    _name = "loan.request"
    _description = "Employee loan request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    name = fields.Char('Description', required=True)
    deduction_method = fields.Selection(selection=[
        ('payroll', 'Payroll'),
        ('cash', 'Cash'),
        ], string="Reimbursement Method"
    )
    partner_id = fields.Many2one('res.partner')
    loan_amount = fields.Monetary('Loan Amount', currency_field='currency_id', tracking=True)
    disburse_amount = fields.Monetary('Loan Amount', currency_field='currency_id', compute="_compute_disburse_amount")
    duration = fields.Integer(string="Duration")
    end_amount = fields.Monetary('End Amount', currency_field='currency_id', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [('readonly', False)], 'refused': [('readonly', False)]}, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env.company.currency_id)
    
    @api.depends("loan_amount", "duration")
    def _compute_disburse_amount(self):
        self.disburse_amount = self.loan_amount / self.duration