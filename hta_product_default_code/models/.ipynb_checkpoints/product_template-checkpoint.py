# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ProductTemplateCustom(models.Model):
    _inherit = "product.template"
    
    
    @api.depends("categ_id")
    def _depends_attribute(self):
        for rec in self:
            if rec.categ_id.attribute_ids:
                caracteriste_lines = [(5,0,0)]
                for line in rec.categ_id.attribute_ids:
                    caracteriste_lines.append((0, 0, {
                        'attribute_id': line.id,
                        'value_ids':line.value_ids,
                    }))
                rec.attribute_line_ids = caracteriste_lines
    
    @api.onchange("categ_id")
    def _onchange_attribute(self):
        for rec in self:
            if rec.categ_id.attribute_ids:
                caracteriste_lines = [(5,0,0)]
                for line in rec.categ_id.attribute_ids:
                    caracteriste_lines.append((0, 0, {
                        'attribute_id': line.id,
                        'value_ids':line.value_ids,
                    }))
                rec.attribute_line_ids = caracteriste_lines


