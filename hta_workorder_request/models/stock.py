# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    product_request_id = fields.Many2one('product.request', string="Work Order")
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_line_id = fields.Many2one('product.request.line', string='Product Request Line')