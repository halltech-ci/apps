# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""
In expense amount is given to employee and employee must justify expense with bill.
If he can not justify employee account is credited with the amount
"""
class HrExpense(models.Model):
    #_name = "hr.expense"
    _inherit = "hr.expense"
    
    payment_mode = fields.Selection([
        ("employee_account", "Employee (To be justify)"),
        ("own_account", "Employee (to reimburse)"),
        ("company_account", "Company")
    ], default='employee_account', states={'done': [('readonly', True)], 'post': [('readonly', True)], 'submitted': [('readonly', True)]}, string="Payment By")
    product_uom_id = fields.Many2one(required=False)
    #quantity = fields.Float(required=False)
    unit_amount = fields.Float(required=False, string="Amount")
    
    