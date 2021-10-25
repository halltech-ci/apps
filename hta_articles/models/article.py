import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models



class ProductTemplate(models.Model):
    _inherit = "product.template"

    code_prefix = fields.Char(compute='_compute_code_prefix', help="Add prefix to product variant reference (default code)",)
    
    code_mesure = fields.Char()
    
    
    
    @api.onchange("categ_id")
    def _compute_code_prefix(self):
        for rec in self:
            if rec.categ_id:
                rec.name = rec.categ_id.recovery_name
                
                
    @api.onchange("categ_id")
    def _compute_code_prefix(self):
        for rec in self:
            if rec.categ_id:
                rec.default_code = rec.categ_id.code_reference2
                
                
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
            rec.resultat = rec.fonctionIcrementation(200)
            rec.code_prefix = rec.resultat