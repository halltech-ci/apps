# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    def _get_default_code(self):
        res = self.env['ir.sequence'].next_by_code('product.default.code')
        return res

    default_code = fields.Char('Internal Reference', index=True, default=_get_default_code)

    _sql_constraints = [
        ('default_code_uniq', 'unique(default_code)',
            'Internal Reference must be unique across the database!'), ]
