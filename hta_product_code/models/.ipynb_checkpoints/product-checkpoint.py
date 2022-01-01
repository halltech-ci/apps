# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_code = fields.Char('Product Code',index=True, compute='_compute_product_code')

    @api.depends('categ_id.related_code')
    def _compute_product_code(self):
        for product in self:
            product.product_code = product.categ_id.related_code