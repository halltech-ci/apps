# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WorkorderSale(models.Model):
    _name = 'workorder.sale'
    _description = "Create sale order from workorder"
    
    
    name = fields.Char()
    code = fields.Char()
    line_ids = fields.One2many('workorder.line', 'workorder_id')
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    
class WorkorderLine(models.Model):
    _name = "workorder.line"
    _description = "workorder sale line"
    
    name = fields.Char(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product')
    product_template_id = fields.Many2one('product.template', string='Product Template', related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    price_subtotal = fields.Monetary(string='Subtotal', store=True)
    currency_id = fields.Many2one(related='workorder_id.currency_id', depends=['company_id.currency_id'], store=True, string='Currency')
    company_id = fields.Many2one(related='workorder_id.company_id', string='Company', store=True, index=True)
    workorder_id = fields.Many2one('workorder.sale', string="Sale workorder", required=True, ondelete="cascade", index=True, copy=False)
    