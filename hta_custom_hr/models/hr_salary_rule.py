# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HrSalaryRule(models.Model):
    _inherit ='hr.salary.rule'
    
    appears_on_paybook = fields.Boolean(string="On Paybook", default=False)
    rubrique = fields.Integer(default=5, help='Use to arrange calculation sequence')
    