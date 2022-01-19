# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = "product.category"
    
    def _get_default_category_code(self):
        return self.env["ir.sequence"].next_by_code("product.category.code")

    category_code = fields.Char(index=True,)
    related_code = fields.Char(string='Related Code', 
                               #compute = '_compute_related_code', 
                               recursive=True, store=True, search='_search_related_field',
                              )
    attribute_lines = fields.One2many('product.attribute.line', 'category_id')
    reference_mask = fields.Char(string="Variant reference mask", copy=False,
        help="Reference mask for building internal references of a "
        "variant generated from this template.\n"
        "Example:\n"
        "A product named ABC with 2 attributes: Size and Color:\n"
        "Product: ABC\n"
        "Color: Red(r), Yellow(y), Black(b)  #Red, Yellow, Black are "
        "the attribute value, `r`, `y`, `b` are the corresponding code\n"
        "Size: L (l), XL(x)\n"
        "When setting Variant reference mask to `[Color]-[Size]`, the "
        "default code on the variants will be something like `r-l` "
        "`b-l` `r-x` ...\n"
        "If you like, You can even have the attribute name appear more"
        " than once in the mask. Such as,"
        "`fancyA/[Size]~[Color]~[Size]`\n"
        " When saved, the default code on variants will be "
        "something like \n"
        ' `fancyA/l~r~l` (for variant with Color "Red" and Size "L") '
        ' `fancyA/x~y~x` (for variant with Color "Yellow" and Size "XL")'
        '\nNote: make sure characters "[,]" do not appear in your '
        "attribute name",
    )
    
    """
    @api.depends("attribute")
    def _compute_value_ids(self):
        for rec in self:
            if rec.attribute:
                rec.value_ids = self.env["product.attribute"].search([('id', "=", rec.attribute.id)]).mapped('value_ids')

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
