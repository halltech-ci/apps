# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WorkorderSale(models.Model):
    _name = 'workorder.sale'
    _description = "Create sale order from workorder"
    
    
    name = fields.Char()
    code = fields.Char()
    line_ids = fields.One2many('workorder.line')
    
    
class WorkorderLine(models.Model):
    _name = "workorder.line"
    
    name = fields.Char(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product')
    product_template_id = fields.Many2one('product.template', string='Product Template', related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    price_subtotal = fields.Monetary(string='Subtotal', store=True)
    