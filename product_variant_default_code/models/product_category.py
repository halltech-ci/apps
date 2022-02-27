# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = "product.category"
    
    def _get_default_category_code(self):
        return self.env["ir.sequence"].next_by_code("product.category.code")

    description = fields.Text()
    category_code = fields.Char(index=True,)
    attribute_lines = fields.One2many('product.attribute.line', 'category_id')
    
    """
    @api.depends("attribute")
    def _compute_value_ids(self):
        for rec in self:
            if rec.attribute:
                rec.value_ids = self.env["product.attribute"].search([('id', "=", rec.attribute.id)]).mapped('value_ids')

    """
    
"""   
class ProductAttributeLine(models.Model):
    _name ="product.attribute.line"
    _description = "Product attribute define in product category"
    
    category_id = fields.Many2one("product.category")
    attribute = fields.Many2one("product.attribute")

    value_ids = fields.Many2many("product.attribute.value", 
                                 #compute="_compute_value_ids"
                                )
    
    @api.onchange("attribute")
    def _onchange_attribute(self):
        if self.attribute:
            self.value_ids = self.env["product.attribute"].search([('id', "=", self.attribute.id)]).mapped('value_ids')
"""

