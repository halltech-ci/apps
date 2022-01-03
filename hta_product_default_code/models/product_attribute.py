# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class hta_product_attribute_value(models.Model):
    _inherit = "product.attribute.value"
    
    @api.depends("attribute_id")
    def _onchange_attribute_code(self):
        if self.attribute_id:
            self.code = self.attribute_id.name[0:2]
        else:
            self.code = "011"
            
    code = fields.Char("Code",default=_onchange_attribute_code,)
    #code_integer = fields.Integer(string="Code Integer")
    
"""    @api.model
    def create(self, vals):
        if "code" not in vals:
            if vals.get('attribute_id'):
                name = vals.get('attribute_id')
                if "natur" in name.name.lower():
                    convert = "0"
                    try:
                        convert = code.code
                        convert = int(convert)+1
                    except:
                        convert = int(convert)+1
                    vals["code"] = convert
        return super(hta_product_attribute_value, self).create(vals)"""
    
    

    
    


