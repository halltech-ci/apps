# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    location_dest_id = fields.Many2one('stock.location', readonly=False)


class StockMoveLine(models.Model):
    _inherit = "stock.move"
    
    product_code = fields.Char(related='product_id.default_code', string="Code Article")