import re
from odoo.exceptions import ValidationError
from collections import defaultdict
from string import Template
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    
    code = fields.Char()
    caracteristique = fields.Char()
    code_reference = fields.Char()
    code_concate = fields.Char() # Concate all code
    
    _sql_constraints = [
        ('code_reference_uniq', 'unique(code_reference)', "Cette page ne peut pas être Dupliquée, Le Code Existe déjâ !"),
    ]
    
    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Cette page ne peut pas être Dupliquée, Le Nom de l'Article Existe déjâ !"),
    ]
    
    
    @api.onchange("categ_id","caracteristique")
    def _onchange_name_(self):
        if self.caracteristique:
            self.name = str(self.categ_id.recovery_name) +' '+ str(self.caracteristique)
        else:
            self.name = self.categ_id.recovery_name
    
#    @api.onchange("categ_id")
    def _get_list_row(self):
#         compte = 0
#         if self.categ_id.code_range == 2:
#             compte = 99
#         elif self.categ_id.code_range == 3:
#             compte = 999
#         elif self.categ_id.code_range == 4:
#             compte = 9999
#         elif self.categ_id.code_range == 5:
#             compte = 99999
#         elif self.categ_id.code_range == 6:
#             compte = 999999
#         else:
#             compte = 999
                   
        res = []
        for i in range(1, 999+1):
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
    
    @api.onchange("categ_id",'code')
    def _onchange_code_concartel(self):
        if self.categ_id:
            self.code_concate = str(self.categ_id.code_concate) + str(self.code)
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
    def _onchange_code_reference(self):
        for rec in self:
            if rec.code_concate:
                result = rec.fonctionTranche(str(rec.code_concate),int(rec.categ_id.code_range))
                rec.code_reference = result
                if rec.code_reference[-1] == '-':
                    rec.code_reference = rec.code_reference.rstrip(rec.code_reference[-1])
            else:
                rec.code_reference = rec.code
            