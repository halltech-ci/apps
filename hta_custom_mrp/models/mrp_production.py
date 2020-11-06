# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    sale_order_id = fields.Many2one('sale.order', string="Commande")
    description = fields.Text("Description")
    mrp_order_line_ids = fields.One2many(related="sale_order_id.order_line", string="Order line", domain=[('in_mrp_line', '=', False)])
    #bom_id = fields.Many2one(required=False)
    
    @api.onchange('sale_order_id')
    def _onchange_sale_order(self):
        if not self.bom_id and self.sale_order_id.sale_mrp_product:
            self.product_id = self.sale_order_id.sale_mrp_product
            self.product_qty = 1.0
