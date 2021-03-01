# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    sde_price_unite = fields.Float(string="Sde Price Unite", store=True, compute='_compute_sde_price')
    
    @api.depends('price_unit','secondary_uom_qty')
    def _compute_sde_price(self):
        for record in self:
            if record.price_unit:
                record.sde_price_unite = (record.price_unit * record.secondary_uom_qty)
            else:
                record.sde_price_unite = 0