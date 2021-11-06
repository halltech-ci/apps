import re
from odoo.exceptions import ValidationError
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    
    
    
    code_prefix = fields.Integer()
    caracteristique = fields.Char()
    code_ref = fields.Char()
    code_referen = fields.Char()
    #code_reference3 = fields.Char(compute='_compute_code_reference3')
    product_reference = fields.Char(string='Article', required=True, copy=False, readonly=True, index=True,
                                   default=lambda self: _('New'))
    
    _sql_constraints = [
        ('code_ref_uniq', 'unique(code_ref)', "Cette page ne peut pas être Dupliquée, Le Code Existe déjâ !"),
    ]
     
    
    @api.onchange("categ_id")
    @api.depends('categ_id.product_count')
    def _onchange_default_code_prefix(self):
        res = []
        for i in range(self.categ_id.product_count, 999+1):
            res.append(i)
        increment = (min(res) + 1)
        self.code_prefix = increment
             
        
    @api.onchange("code_prefix")
    def _onchange_code_prefix(self):
        for rec in self:
            converts = str(rec.code_prefix)
        if len(converts) == 1:
            converts = '00' + str(converts)
        if len(converts) == 2:
            converts = '0' + str(converts)
        if rec.code_prefix:
            rec.code_referen = converts
        else:
            self.code_referen = converts
       
    @api.depends("categ_id")
    def _compute_barcode(self):
        for rec in self:
            if rec.categ_id:
                rec.barcode = rec.code_prefix
            
            
    #affichage du name
    @api.onchange("categ_id","caracteristique")
    def _onchange_name_(self):
        if self.caracteristique:
            self.name = str(self.categ_id.recovery_name) +' '+ str(self.caracteristique)
        else:
            self.name = self.categ_id.recovery_name
        
    
    @api.onchange('categ_id','code_referen')
    @api.depends('code_referen', 'categ_id')
    def _onchange_code_ref(self):
        for rec in self:
            if rec.code_referen:
                rec.code_ref = str(rec.categ_id.code_references) + str(rec.code_referen)
            else:
                rec.code_ref = '%s' %(rec.code_referen)
    
#     @api.onchange('code_prefix')
#     def onchange_code_ref(self):
#         for rec in self:
#             if rec.code_prefix:
#                 rec.code_ref = str(rec.categ_id.code_references) + str(rec.code_prefix)
#             else:
#                 rec.code_ref = '%s' %(rec.code_prefix)
        
#     @api.onchange('categ_id.code_references')
#     def onchange_code_ref(self):
#         for rec in self:
#             if rec.categ_id:
#                 rec.code_ref = str(rec.categ_id.code_references) + str(rec.code_prefix)
#             else:
#                 rec.code_ref = '%s' %(rec.code_prefix)
                
                
                
#     def _search_prefix_field(self, operator, value):
#         return [('code_prefix', operator, value)]
    
    
    
    
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
#     @api.model
#     def create(self, vals):
#         if vals.get('product_reference', _('New')) == _('New'):
#             vals['product_reference'] = self.env['ir.sequence'].next_by_code('product_reference.code') or _('New')
#         result = super(ProductTemplate, self).create(vals)
#         return result
    
    
#     @api.depends("product_reference")
#     def _compute_code_prefix(self):
#         for rec in self:
#             rec.code_prefix = rec.product_reference
    

    
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