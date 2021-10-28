import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError



class ProductTemplate(models.Model):
    _inherit = "product.template"
    
   
    #code_prefix = fields.Char()
    code_prefix = fields.Char(compute='_compute_code_prefix', help="Add prefix to product variant reference (default code)")
    code_mesure = fields.Char()
    code_ref = fields.Char(compute='_compute_code_ref')
    product_reference = fields.Char(string='Article', required=True, copy=False, readonly=True, index=True,
                                   default=lambda self: _('New'))
    groupement = fields.Integer(default=3)
    
    
    
    
    #code article reference
    @api.model
    def create(self, vals):
        if vals.get('product_reference', _('New')) == _('New'):
            vals['product_reference'] = self.env['ir.sequence'].next_by_code('product_reference.code') or _('New')
        result = super(ProductTemplate, self).create(vals)
        return result
    
    
    @api.depends("product_reference")
    def _compute_code_prefix(self):
        for rec in self:
            rec.code_prefix = rec.product_reference
            
            
     # affichage du name
    @api.onchange("categ_id","code_mesure")
    def _onchange_name_(self):
        self.name = str(self.categ_id.recovery_name) +' '+ str(self.code_mesure) 
    
#     @api.depends("categ_id","code_prefix")
#     def _compute_code_prefix(self):
#         for rec in self:
#             rec.code_prefix = rec.product_reference


    def fonctionTranche(self,liste, groupement):
        res = ""
        cpt = 0
        for l in range(0,len(liste)):
            res = res + liste[l]
            cpt = cpt + 1
            if cpt == groupement:
                res = res + "-"
                cpt = 0
        return res

    @api.depends("code_prefix","categ_id")
    def _compute_code_ref(self):
        for rec in self:
            if rec.code_prefix == "New":
                rec.code_ref =  str(rec.categ_id.code_reference2)
            else:
                rec.resultat = rec.fonctionTranche(str(rec.code_prefix),rec.groupement)
                rec.code_reference = rec.resultat
                rec.code_ref =  str(rec.categ_id.code_reference2) +str(rec.resultat)

        
   
    
#     @api.onchange("code_ref")
#     def _compute_code_reference(self):
#         for rec in self:
#             rec.resultat = rec.fonctionTranche(str(rec.code_ref),rec.groupement)
#             rec.code_reference = rec.resultat