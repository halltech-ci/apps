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


class AccountAssetAsset(models.Model):
    _inherit = "account.asset.asset"
    
    date = fields.Date('Asset Starting date', related="invoice_id.asset_date")
    