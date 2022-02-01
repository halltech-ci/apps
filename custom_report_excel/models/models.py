# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_report_excel(models.Model):
#     _name = 'custom_report_excel.custom_report_excel'
#     _description = 'custom_report_excel.custom_report_excel'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
