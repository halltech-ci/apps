import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models



class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    name = fields.Char('Name', index=True, required=True, translate=True, compute='_compute_name')
    code_prefix = fields.Char(compute='_compute_code_prefix', help="Add prefix to product variant reference (default code)",)
    
    code_mesure = fields.Char()
    
    
    
    @api.depends("categ_id")
    def _compute_name(self):
        for rec in self:
            if rec.categ_id:
                if rec.code_mesure is False:
                    rec.name = rec.categ_id.recovery_name 
                else:
                    rec.name = rec.categ_id.recovery_name +' '+ str(rec.code_mesure) 
                
    def fonctionIcrementation(self, n):
        for i in range(1, n+1):
            if len(str(i))<len(str(n)):
                reste = len(str(n))-len(str(i))
                nombre = "0"*reste + str(i)
                return nombre
            else:
                return i          
    @api.model
    def _compute_code_prefix(self):
        for rec in self:
            rec.resultat = rec.fonctionIcrementation(999)
            rec.code_prefix = rec.resultat
            
    @api.depends("categ_id")
    def _compute_default_code(self):
        for rec in self:
            rec.resultat = rec.fonctionIcrementation(999)
            if rec.categ_id:
                rec.default_code = rec.categ_id.code_reference2 +str(rec.resultat)
                