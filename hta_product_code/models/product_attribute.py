# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

_VALUE_COMPUTE_PARAMETER = [('troncate')]


class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    
    category_id = fields.Many2one("product.category")
    code_type = fields.Selection(selection=([('number', 'numerique'), ('char', 'Alphanumerique')]), string="Type Code")
    code_length = fields.Integer(default=2, string="Nombre de caractere")
    is_automatic_code = fields.Boolean(default=True, string="Automatique/Manuel")
    code_compute_parameter = fields.Char(string="Parametre")
    
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.code = self.name[0:2]
    
    code = fields.Char(compute="_compute_value_code", default=_onchange_name, string="Code", store=True)
    
    
    @api.depends('attribute_id.code_compute_parameter', 'name')
    def _compute_value_code(self):
        if self.name:
            parameter = self.attribute_id.code_compute_parameter
            self.code = self.name[0:2]
    
    