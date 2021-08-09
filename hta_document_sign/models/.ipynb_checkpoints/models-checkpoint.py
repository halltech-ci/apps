# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hta_document_sign(models.Model):
#     _name = 'hta_document_sign.hta_document_sign'
#     _description = 'hta_document_sign.hta_document_sign'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
