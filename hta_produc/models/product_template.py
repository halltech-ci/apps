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
    groupement = fields.Integer(default=3)
    code_referen = fields.Char()
    code_concartel = fields.Char()
    product_reference = fields.Char(string='Article', required=True, copy=False, readonly=True, index=True,
                                   default=lambda self: _('New'))
    
    _sql_constraints = [
        ('code_ref_uniq', 'unique(code_ref)', "Cette page ne peut pas être Dupliquée, Le Code Existe déjâ !"),
    ]
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Cette page ne peut pas être Dupliquée, Le Nom Existe déjâ !"),
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
            
            
    @api.onchange("categ_id","code_referen")
    def _onchange_code_concartel(self):
        if self.categ_id:
            self.code_concartel = str(self.categ_id.code_reference)+ str(self.code_referen)
        else:
            self.code_concartel = self.code_referen
    
                
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
    @api.onchange('code_concartel','code_referen')
    @api.depends("categ_id")
    def _onchange_code_ref(self):
        for rec in self:
            if rec.code_concartel:
                rec.resultat = rec.fonctionTranche(str(rec.code_concartel),int(rec.categ_id.code_range))
                #rec.code = rec.resultat.rstrip(rec.resultat[-1])
                #rec.code_ref = rec.code
                rec.code_ref = rec.resultat
            else:
                rec.code_ref = rec.code_referen