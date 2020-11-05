# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = "mrp.production"
    
    sale_order = fields.Many2one('sale.order', string="Commande")
    description = fields.Text("Description")
    mrp_order_line_ids = fields.One2many('mrp.order.line', 'mrp_production_id', string="Order line")
    bom_id = fields.Many2one(required=False)
    
    @api.onchange('sale_order')
    def _onchange_sale_order(self):
        if self.sale_order.sale_mrp_product:
            self.product_id = self.sale_order.sale_mrp_product
    

class MrpOrderLine(models.Model):
    _name = "mrp.order.line"
    _description = "MRP order line"
    
    mrp_production_id = fields.Many2one('mrp.production', string='Product ID')
    product_id = fields.Many2one("product.product", string='Product')
    product_uom_qty = fields.Float('Quantity')
    
    
    
    
    