# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Picking(models.Model):
    _inherit = "stock.picking"
    
    product_request_id = fields.Many2one('product.request', string="Product Request",
            related='move_lines.product_line_id.request_id',
    )
    def button_validate(self):
        self.product_request_id._action_done()
        return super(Picking, self).button_validate()
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_line_id = fields.Many2one('product.request.line', string='Product Request Line')
    