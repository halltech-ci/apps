import re
from odoo.exceptions import ValidationError
from collections import defaultdict
from string import Template
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    def _get_product_type_row(self):
        type_product = self.categ_id.type_category_ids
        return type_product

    code = fields.Char()
    caracteristique = fields.Char()
    code_reference = fields.Char()
    code_concate = fields.Char() # Concate all code
    type_id = fields.Many2one("product.category.type")
    
    
    _sql_constraints = [
        ('code_reference_uniq', 'unique(code_reference)', "Cette page ne peut pas être Dupliquée, Le Code de l'Article Existe déjâ !"),
    ]
    
    _sql_constraints = [
        ('caracteristique_uniq', 'unique(caracteristique)', "Cette page ne peut pas être Dupliquée, Ces Caractreristiques Existe déjâ !"),
    ]
    
    @api.onchange("categ_id")
    def _onchange_type_product_id(self):
        if self.categ_id:
            type_products = self.categ_id.type_category_ids.ids
            if type_products: 
                domain = [('id','in',type_products)]
                return  {'domain':{'type_id':domain}}
        return  {'domain':{'type_id':[('id', 'in', [])]}}
    
    @api.onchange("categ_id","caracteristique","type_id")
    def _onchange_name_(self):
        if self.categ_id:
            self.name = str(self.categ_id.recovery_name) + ' '+ str(self.caracteristique) 
        if self.type_id:
            self.name = str(self.categ_id.recovery_name) + ' ' + str(self.type_id.name) +' '+ str(self.caracteristique)
        if self.caracteristique:
            self.name = str(self.categ_id.recovery_name) + ' ' + str(self.type_id.name) +' '+ str(self.caracteristique)
        
    
    def _get_list_row(self):
        code_category = str(self.categ_id.code_concate)
        code_type = str(self.type_id.code)
        code_concate_category = code_category + code_type
        compte = 999
        tranche = 3
        if len(code_concate_category) <= 12:
            tranche = 12 - len(code_concate_category)
        if tranche == 2:
            compte = 99
        elif tranche == 3:
            compte = 999
        elif tranche == 4:
                compte = 9999
        elif tranche == 5:
                compte = 99999
        elif tranche == 6:
            compte = 999999
        else:
            compte = 999999
        res = []
        for i in range(1, compte+1):
            converts = str(i)
            if len(converts) == 1:
                converts = '00' + str(converts)
            if len(converts) == 2:
                converts = '0' + str(converts)
            res.append(converts)
        
        return res
    
    
    @api.onchange("categ_id")
    @api.depends('categ_id')
    def _get_list_category(self):
        results = self._get_list_row() 
        res = []
        for rs in results:
            for rq in self.categ_id.template_code:
                requests = self.env['product.template'].search_read([('id','=',rq.id)])
                for rs_code in requests:
                    res.append(rs_code.get('code'))
            if rs not in res:
                self.code = rs
                break
            res.clear()
    
    @api.onchange("categ_id",'type_id','code')
    def _onchange_code_concartel(self):
        if self.categ_id:
            self.code_concate = str(self.categ_id.code_concate) + str(self.code)
        if self.type_id:
            self.code_concate = str(self.categ_id.code_concate) + str(self.type_id.code) + str(self.code)
        else:
            self.code_concate = self.code
    
                
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
    
    @api.onchange('code_concate')
    @api.depends("categ_id")
    def _onchange_code_ref(self):
        for rec in self:
            if rec.code_concate:
                result = rec.fonctionTranche(str(rec.code_concate),int(rec.categ_id.code_range))
                rec.code_reference = result
                if rec.code_reference[-1] == '-':
                    rec.code_reference = rec.code_reference.rstrip(rec.code_reference[-1])
            else:
                rec.code_reference = rec.code
            