# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_code = fields.Char('Product Code',index=True, compute='_compute_product_code')

    @api.depends('categ_id.related_code')
    def _compute_product_code(self):
        for product in self:
            product.product_code = product.categ_id.related_code
    
    @api.depends("categ_id")
    def _depends_attribute(self):
        for rec in self:
            if rec.categ_id.attribute_lines:
                lines = [(5,0,0)]
                for line in rec.categ_id.attribute_lines:
                    lines.append((0, 0, {
                        'attribute_id': line.id,
                        'value_ids':line.value_ids,
                    }))
                rec.attribute_line_ids = lines