# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequestType(models.Model):
    _name = 'purchase.request.type'
    _description = "Purchase type. Configure different purchase type base on product category"
    
    
    name = fields.Char(required=True)
    product_category = fields.Many2one('product.category', string='Product Category')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company,)
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description", translate=True)