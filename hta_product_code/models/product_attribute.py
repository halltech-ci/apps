# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

_VALUE_COMPUTE_PARAMETER = [('troncate')]


class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    
    category_id = fields.Many2one("product.category")
    code_type = fields.Selection(selection=([('number', 'numerique'), ('char', 'Alphanumerique')]), string="Type Code")
    code_length = fields.Integer(default=2, string="Nombre de caractere")
    is_automatic_code = fields.Boolean(default=True, string="Automatique/Manuel")
    code_compute_parameter = fields.Text(string="Parametre")
    
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    code = fields.Char(compute="_compute_value_code", string="Code")
    
    
    #@api.depends('is_automatic_code')
    def _compute_value_code(self):
        pass
    
    