# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""Provide integration between HR Expense application and HR Payroll to move HR expense not justify to employee
account.
"""
class HrContract(models.Model):
    _inherit = "hr.contract"
    
    