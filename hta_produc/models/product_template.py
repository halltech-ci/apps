import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models



class ProductTemplate(models.Model):
    _inherit = "product.template"

    code_prefix = fields.Char(compute='_compute_code_prefix', help="Add prefix to product variant reference (default code)")
    code_mesure = fields.Char()
    #product_reference = fields.Char(string='Article',required=True,copy=False, readonly=True,index=True,default=lambda self: _('New'))
    
    _sql_constraints = [
        ('name_unique', 'unique (name)', "Ce Mon Existe déjâ!")
    ]
    
    
    # affichage du name
    @api.onchange("categ_id","code_mesure")
    def _onchange_name_(self):
        self.name = str(self.categ_id.recovery_name) +' '+ str(self.code_mesure) 
                
                
                    
    #code article reference
    #@api.model
    #def create(self, vals):
        #if vals.get('product_reference', _('New')) == _('New'):
            #vals['product_reference'] = self.env['ir.sequence'].next_by_code('product_reference.code') or _('New')
        #result = super(ProductTemplate, self).create(vals)
        #return result
         
    
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
            
    
    
    
    #code article reference
    #@api.model
    #def create(self, vals):
        #if vals.get('product_reference', _('New')) == _('New'):
            #vals['product_reference'] = self.env['ir.sequence'].next_by_code('product_reference.code') or _('New')
        #result = super(ProductTemplate, self).create(vals)
        #return result
    
    #code article(default_code)
    #@api.onchange("categ_id")
    #def _onchange_default_code(self):
        #for rec in self:
            #if rec.categ_id:
                #rec.default_code =rec.categ_id.code_reference2 + rec.code_prefix
       
    #@api.onchange("categ_id")
    #def _onchange_default_code(self):
        #for rec in self:
            #if rec.categ_id:
                #rec.default_code =rec.categ_id.code_reference2 + rec.code_prefix      
    
    #def fonctionIcrementation(self, n):
        #for i in range(1, n+1):
            #if len(str(i))<len(str(n)):
                #reste = len(str(n))-len(str(i))
                #nombre = "0"*reste + str(i)
                #return nombre
            #else:
                #return i          
    #@api.model
    #def _compute_code_prefix(self):
        #for rec in self:
            #rec.resultat = rec.fonctionIcrementation(999)
            #rec.code_prefix = rec.resultat
            
    #@api.depends("categ_id")
    #def _compute_default_code(self):
        #for rec in self:
            #rec.resultat = rec.fonctionIcrementation(999)
            #if rec.categ_id:
                #rec.default_code = rec.categ_id.code_reference2 +str(rec.resultat)