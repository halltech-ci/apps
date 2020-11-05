# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    #description = fields.Text('Description')
    sale_mrp_product = fields.Many2one('product.product', ondelete='cascade')
    #mrp_bom_id = fields.Many2one("mrp.bom")
    #sale_mrp = fields.Many2one('mrp.production')
    
    """
    Create BOM associated to the SO. 
    """
    def create_sale_mrp_product(self):
        '''create product template for coresponding sale_order'''
        product_product = self.env['product.product']
        for order in self:
            if not order.sale_mrp_product and order.description:
                product_name = order.description
                route_id = self.env['stock.location.route'].search([('name', '=', 'Manufacture')]).id
                route = []
                route_ids = route.append(route_id)
                product_prod = product_product.create({
                    'name': product_name,
                    'type': 'product',
                    'purchase_ok': False,
                    'categ_id': 1,
                    'route_ids': route_ids
                })
            order.sale_mrp_product = product_prod
            
    
        
            
                
        
            
        
    