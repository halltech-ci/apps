# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = "product.category"
    

    description = fields.Text()
    category_code = fields.Char(index=True,)
    

    @api.depends("attribute")
    def _compute_value_ids(self):
        for rec in self:
            if rec.attribute:
                rec.value_ids = self.env["product.attribute"].search([('id', "=", rec.attribute.id)]).mapped('value_ids')

