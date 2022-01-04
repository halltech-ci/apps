# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class hta_product_attribute_value(models.Model):
    _inherit = "product.attribute.value"
    
#     @api.onchange("name")
#     def _onchange_attribute_code(self):
#         if self.attribute_id:
#             convert = "1"
#             attribute_id = self.attribute_id.id
#             req = self.env['product.attribute.value'].search([('attribute_id','=',attribute_id)],order='create_date desc', limit=1)
#             if req:
#                 for code in req:
#                     if "natur" in code.attribute_id.name.lower():
#                         convert = code.code
#                 try:
#                     convert = int(convert)+1
#                 except:
#                     convert = int(convert)+1
#                 self.code = str(convert)
#             else:
#                 self.code = str(convert)
            
    code = fields.Char("Code Variante")
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
    
    

    
    


