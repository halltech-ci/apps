import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models



class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    
    code_prefix = fields.Char(compute='_compute_code_prefix', help="Add prefix to product variant reference (default code)")
    caracteristique = fields.Char()
    code_ref = fields.Char(compute='_compute_code_ref')
    #code_referen = fields.Char(compute='_compute_code_referen')
    #code_reference3 = fields.Char(compute='_compute_code_reference3')
    product_reference = fields.Char(string='Article', required=True, copy=False, readonly=True, index=True,
                                   default=lambda self: _('New'))
    
    
#     @api.constrains('name')
#     def _check_name(self):
#         for rec in self:
#             article = self.env['product.template'].search([('name','=',rec.name), ('id','!=',rec.id)])
#             if article:
#                 raise ValidationError(_("Name %s existe déjà" % rec.name))
    
#     @api.constrains('name')
#     def _check_unique_code_mesure(self):
#         names = self.search([]) - self
#         values = [ x.name.lower() for x in names ]
        
#         if self.name and self.name.lower() in values:
#             raise ValidationError(_('article already exists!'))
	
#         return True


    
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
            
            
    #affichage du name
    @api.onchange("categ_id","caracteristique")
    def _onchange_name_(self):
        self.name = str(self.categ_id.recovery_name) +' '+ str(self.caracteristique) 
        
        
#         if self.name is True:
#             raise ValidationError(_('Name product already exists!'))
            
        
        

    @api.depends("code_prefix","categ_id")
    def _compute_code_ref(self):
        for rec in self:
            if rec.code_prefix == "New":
                rec.code_ref =  rec.fonctionTranche(rec.categ_id.code_reference)
            else:
                concat = str(rec.categ_id.code_reference) +'-'+ str(rec.code_prefix)
                #resultat = rec.fonctionTranche(concat)
                rec.code_ref = str(concat)

    
#     @api.depends("categ_id","code_prefix")
#     def _compute_code_prefix(self):
#         for rec in self:
#             rec.code_prefix = rec.product_reference

#     @api.depends("code_prefix","categ_id")
#     def _compute_code_reference(self):
#         for rec in self:
#             if rec.code_prefix == "New":
#                 rec.code_ref =  str(rec.categ_id.code_reference2)
#             else:
#                 rec.code_prefix = rec.code_ref
                
                
#     @api.onchange("code_prefix","categ_id")
#     def _compute_code_referen(self):
#         for rec in self:
#             if rec.categ_id:
#                 rec.code_referen =  str(rec.categ_id.code_reference)+ str(rec.code_prefix)
              
            
            
            
#     def fonctionTranche(self,liste, groupement):
#         res = ""
#         cpt = 0
#         for l in range(0,len(liste)):
#             res = res + liste[l]
#             cpt = cpt + 1
#             if cpt == groupement:
#                 res = res + "-"
#                 cpt = 0
#         return res
    
#     @api.onchange("code_referen")
#     def _compute_code_reference3(self):
#         for rec in self:
#             rec.resultat = rec.fonctionTranche(str(rec.code_referen),rec.groupement)
#             rec.code_reference3 = rec.resultat
            
        
   
    
#     @api.onchange("code_ref")
#     def _compute_code_reference(self):
#         for rec in self:
#             rec.resultat = rec.fonctionTranche(str(rec.code_ref),rec.groupement)
#             rec.code_reference = rec.resultat