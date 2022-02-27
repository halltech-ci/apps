# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = "product.category"
    

    description = fields.Text()
    category_code = fields.Char(index=True,)
    #attribute_lines = fields.One2many('product.attribute.line', 'category_id')
    