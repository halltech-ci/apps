# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = "stock.move"
    
    product_code = fields.Char(related='product_id.default_code', string="Code Article")