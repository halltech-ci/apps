# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hta_product_default_code(models.Model):
#     _name = 'hta_product_default_code.hta_product_default_code'
#     _description = 'hta_product_default_code.hta_product_default_code'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
