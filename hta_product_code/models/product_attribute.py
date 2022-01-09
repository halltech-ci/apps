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
    last_code = fields.Integer(string="Last Value Code", compute="_compute_last_value_code")
    
    def _compute_last_value_code(self):
        for rec in self:
            code = rec.mapped('value_ids').sort(reverse=True)
            self.last_code = int([0]) or 1
    
    def _recuperate_compute_parameter(self):
        if self.code_compute_parameter:
            convertedDict = dict((x.strip(), (y.strip()))
                     for x, y in (element.split(':')
                                  for element in self.code_compute_parameter.split(',')))
            return convertedDict
        
    def _compute_code(self):
        for rec in self:
            parametre = rec._recuperate_compute_parameter()
            val = 1
            if "incr" in parametre:
                val = int(parametre.get('incr'))
                code = val
                for line in rec.value_ids:
                    line.code = code 
                    code += val
    
    def write(self, line_values):
        res = super(ProductAttribute, self).write(line_values)
        self._compute_code()
        return res
    
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    code = fields.Char(string="Code", store=True)
    