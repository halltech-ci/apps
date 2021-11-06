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