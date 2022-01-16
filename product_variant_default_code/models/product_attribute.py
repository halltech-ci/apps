# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

_VALUE_COMPUTE_PARAMETER = [('troncate')]


class ProductAttribute(models.Model):
    _inherit = "product.attribute"
    
    #category_id = fields.Many2one("product.category")
    code_type = fields.Selection(selection=([('number', 'numerique'), ('char', 'Alphanumerique')]), string="Type Code")
    code_length = fields.Integer(default=2, string="Nombre de caractere")
    is_automatic_code = fields.Boolean(default=True, string="Automatique/Manuel")
    code_compute_parameter = fields.Char(string="Parametre")
    last_code = fields.Integer(string="Last Value Code", compute="_compute_last_value_code")
    #product_tmpl_id = fields.Many2one("product.template", compute="_compute_attribute_id")
    
    
    
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
            if rec.code_compute_parameter:
                param = rec._recuperate_compute_parameter()
                val = 1
                if "incr" in param:
                    val = int(param.get('incr'))
                    code = val
                    for line in rec.value_ids:
                        if not line.is_manual:
                            line.code = code
                            code += val
                if "pre" in param:
                    val = param.get('pre')
                    for line in rec.value_ids:
                        if not line.is_manual:
                            line.code = "{0}{1}".format(val, line.name)
                if "tronc" in param:
                    val = int(param.get('tronc'))
                    for line in rec.value_ids:
                        if not line.is_manual:
                            line.code = line.name[0:val]
    
    def write(self, line_values):
        res = super(ProductAttribute, self).write(line_values)
        self._compute_code()
        return res
    
    
class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    code = fields.Char(string="Code", store=True,)
    is_manual = fields.Boolean(default=False)
    
    """
    @api.onchange('name')
    def _onchange_name(self):
        self.code = self.attribute_id._compute_code()
    """
    
    
    
    