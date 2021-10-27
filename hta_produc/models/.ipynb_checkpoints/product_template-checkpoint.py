import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models



class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    @api.constrains('name')
    def _check_mobile_unique(self):
        name_counts = self.search_count([('name', '=', self.name), ('id', '!=', self.id)])
        print(name_counts)
        if name_counts > 0:
            raise ValidationError("Name article already exists!")
    
    code_prefix = fields.Char(compute='_compute_code_prefix', help="Add prefix to product variant reference (default code)")
    code_mesure = fields.Char()
    
    
    # affichage du name
    @api.onchange("categ_id","code_mesure")
    def _onchange_name_(self):
        self.name = str(self.categ_id.recovery_name) +' '+ str(self.code_mesure) 
                
    
    @api.depends("categ_id")
    def _compute_code_prefix(self):
        req = self.env['product.template'].search([('categ_id','=',self.categ_id.id)])
        increment = len(req) + 1
        converts = str(increment)
        if len(converts) == 1:
            converts = '00' + str(converts)
        if len(converts) == 2:
            converts = '0' + str(converts)
        if self.categ_id:
            self.code_prefix = self.categ_id.code_reference2 + converts
        else:
            self.code_prefix = converts
