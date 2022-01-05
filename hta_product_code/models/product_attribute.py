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
    
    def _recuperate_compute_parameter(self):
        if self.code_compute_parameter:
            convertedDict = dict((x.strip(), int(y.strip()))
                     for x, y in (element.split(':')
                                  for element in self.code_compute_parameter.split(', ')))
            return convertedDict
    
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    def increment(self, val):
        #domaine = [()]
        last_code = self.env['product.attribute.value'].search([('attribute_id', '=', self.attribute_id.id)], order="code desc",limit=1)
        code ="0"
        if last_code:
            code = int(last_code.code) + int(val)
        else:
            code = last_code
        return str(code)
    
    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            param = self.attribute_id._recuperate_compute_parameter()
            if param:
                if 'incr' in param:
                    self.increment(param.get('incr'))
                    self.code = self.increment(param.get('incr'))
                if 'tronc' in param:
                    val = param.get('tronc')
                    self.code = self.name[0:val]
                if 'pre' in param:
                    val = param.get('tronc')
                    self.code = "{0}{1}".format(val, self.name)
    
    
#     @api.onchange('name')
#     def _onchange_name(self):
#         if self.name:
#             self.code = self.name[0:2]
    
    code = fields.Char(default=_onchange_name, string="Code", store=True)
    
    
#     @api.depends('attribute_id.code_compute_parameter', 'name')
#     def _compute_value_code(self):
#         for val in self:
#             parameter = val.attribute_id.code_compute_parameter
#             if val.name:
#                 parameter = val.attribute_id.code_compute_parameter
#                 val.code = val.name[0:2]
    
    