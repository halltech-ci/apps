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
    attribute_lines = fields.One2many('product.attribute', 'category_id')
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
    @api.depends('parent_id.related_code', 'category_code')
    def _compute_related_code(self):
        for category in self:
            if category.parent_id:
                category.related_code = '%s%s' % (category.parent_id.related_code, category.category_code)
            else:
                category.related_code = '%s' %(category.category_code)
    """
    """
    @api.onchange('parent_id')
    def onchange_parent_id(self):
        for category in self:
            if category.parent_id:
                category.related_code = '%s%s' % (category.parent_id.related_code, category.category_code)
            else:
                category.related_code = '%s' % (category.category_code)
    """

    """
    @api.onchange('category_code')
    def onchange_category_code(self):
        for category in self:
            if category.parent_id:
                category.related_code = '%s%s' % (category.parent_id.related_code, category.category_code)
            else:
                category.related_code = '%s' % (category.category_code)

    def _search_related_field(self, operator, value):
        return [('related_code', operator, value)]
    """
    """
    _sql_constraints = [
        ('related_code_uniq', 'unique(related_code)', "Related_code must be unique !"),
    ]
    """
    