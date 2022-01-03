# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _order = 'number asc, order_id, id'
    
    # displays sequence on the order line
    number = fields.Integer(help="Shows the sequence of this line in the sale order.", related='sequence', string="N° ligne", store=True)

    @api.model
    def create(self, values):
        line = super(SaleOrderLine, self).create(values)
        return line