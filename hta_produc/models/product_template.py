import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError



class ProductTemplate(models.Model):
    _inherit = "product.template"
    
   
    code_prefix = fields.Char()
    code_mesure = fields.Char()
    
    
    # affichage du name
    @api.onchange("categ_id","code_mesure")
    def _onchange_name_(self):
        
        self.name = str(self.categ_id.recovery_name) +' '+ str(self.code_mesure) 
    
#     @api.onchange("categ_id")
#     def _onchange_code_prefix(self):
#         req = self.env['product.template'].search([('categ_id','=',self.categ_id.id)])
#         increment = len(req) + 1
#         converts = str(increment)
#         if len(converts) == 1:
#             converts = '00' + str(converts)
#         if len(converts) == 2:
#             converts = '0' + str(converts)
        
#         self.code_prefix = converts

    
