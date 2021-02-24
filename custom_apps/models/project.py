# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


# class custom_apps(models.Model):
#     _name = 'custom_apps.custom_apps'
#     _description = 'custom_apps.custom_apps'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class Project(models.Model):
    _inherit = "project.project"
    
    sale_order_ids = fields.One2many(comodel_name = "sale.order", inverse_name = "project_id", string="Sale Orders")
    