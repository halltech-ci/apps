# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class hta_custom_hr(models.Model):
#     _name = 'hta_custom_hr.hta_custom_hr'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class HrContract(models.Model):
    _inherit = "hr.contract"
    
    hourly_rate = fields.Monetary(string="Hourly Cost", compute="_compute_employee_hourly_rate")
    
    @api.depends("wage")
    def _compute_employee_hourly_rate(self):
        for rec in self:
            rec.hourly_rate = rec.wage/173.33