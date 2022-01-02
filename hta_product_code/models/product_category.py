# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = "product.category"
    
    def _get_default_category_code(self):
        return self.env["ir.sequence"].next_by_code("product.category.code")

    category_code = fields.Char(index=True,)
    related_code = fields.Char(string='Related Code', compute = '_compute_related_code', recursive=True, store=True, search='_search_related_field',)

    @api.depends('parent_id.related_code', 'category_code')
    def _compute_related_code(self):
        for category in self:
            if category.parent_id:
                category.related_code = '%s%s' % (category.parent_id.related_code, category.category_code)
            else:
                category.related_code = '%s' %(category.category_code)

    @api.onchange('parent_id')
    def onchange_parent_id(self):
        for category in self:
            if category.parent_id:
                category.related_code = '%s%s' % (category.parent_id.related_code, category.category_code)
            else:
                category.related_code = '%s' % (category.category_code)

    @api.onchange('category_code')
    def onchange_category_code(self):
        for category in self:
            if category.parent_id:
                category.related_code = '%s%s' % (category.parent_id.related_code, category.category_code)
            else:
                category.related_code = '%s' % (category.category_code)

    def _search_related_field(self, operator, value):
        return [('related_code', operator, value)]
    
    
    _sql_constraints = [
        ('related_code_uniq', 'unique(related_code)', "Related_code must be unique !"),
    ]
    
    