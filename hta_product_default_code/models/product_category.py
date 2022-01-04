# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ProductCategoryCustom(models.Model):
    _inherit = "product.category"
    
    is_virtual_product = fields.Boolean()
    attribute_ids = fields.Many2many('product.attribute')
    


