# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class hta_custom_expense(models.Model):
#     _name = 'hta_custom_expense.hta_custom_expense'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class HrExpense(models.Model):
    #_name = "hr.expense"
    _inherit = "hr.expense"
    
    payment_mode = fields.Selection([
        ("employee_account", "Employee (to justify)"),
        ("own_account", "Employee (to reimburse)"),
        ("company_account", "Company")
    ], default='own_account', states={'done': [('readonly', True)], 'post': [('readonly', True)], 'submitted': [('readonly', True)]}, string="Payment By")
    
    #employee_id = fields.Many2one(string="AssignTo")
    #requested_by = fields.Many2one('hr.employee', string="Requested By", required=True, readonly=True, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1))