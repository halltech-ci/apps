# -*- coding: utf-8 -*-

from datetime import datetime, date
from odoo import models, fields, api


class hta_loan_employee(models.Model):
    _name = 'hr.loan.employee'
    _description = 'hta loan employee'

    name = fields.Char(string='Value', required=True, translate=True)
    amount_loan = fields.Monetary('Amount Loan', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today)
    end_date = fields.Date(string='Date End')
    amount_to_debited = fields.Monetary('Amount to be debited', required=True)
    #amount_debit = fields.Monetary('Amount debited', required=True)
    status = fields.Boolean('Active',default=False, store=True,)
    hr_contract_id = fields.Many2one('hr.contract', string = 'Contract Employee', ondelete='cascade', index=True)
    company_id = fields.Many2one('res.company', readonly=False, default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True)
    
    @api.depends('end_date')
    def _compute_status(self):
        for record in self:
            if record.end_date == date.today():
                record.status = True
                
                
    @api.depends('status')
    def _compute_amount_to_debited(self):
        for record in self:
            if record.status == True:
                record.amount_to_debited = 0
            


