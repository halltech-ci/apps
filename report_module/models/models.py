# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class report_module(models.Model):
#     _name = 'report_module.report_module'
#     _description = 'report_module.report_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
