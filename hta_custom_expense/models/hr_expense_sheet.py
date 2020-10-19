# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval
from odoo.tools import pycompat
from odoo.exceptions import ValidationError

class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    amount_advance = fields.Monetary(string="Advanced Amount", compute="_compute_advance_amount")
    justify_amount = fields.Monetary(string="Justified Amount")
    amount_residual = fields.Monetary(string="Residual Amount", compute="_compute_residual_amount", readonly=True)
    assigned_to = fields.Many2one('hr.employee', string="Beneficiaire")
    employee_id = fields.Many2one(string="Destinataire")
    
    
    @api.one
    @api.depends('expense_line_ids')
    def _compute_advance_amount(self):
        sum_amount = 0.0
        for sheet in self:
            line = self.expense_line_ids.filtered(lambda e:e.payment_mode == 'employee_account')
            if line:
                amount = line.total_amount
                sum_amount += amount 
            else:
                amount = 0.0
            self.amount_advance = sum_amount
            
    @api.one
    @api.depends('amount_advance', 'total_amount')
    def _compute_residual_amount(self):
        for sheet in self:
            self.amount_residual = self.total_amount - self.justify_amount
    
    @api.onchange('justify_amount')
    def onchange_justify_amount(self):
        self.amount_residual = self.total_amount - self.justify_amount
    
    