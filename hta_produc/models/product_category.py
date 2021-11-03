from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CodeCategorie(models.Model):
    _inherit = 'product.category'
    
    def _get_default_category_code(self):
        return self.env["ir.sequence"].next_by_code("product.category.code")

    category_code = fields.Char()
    code_reference = fields.Char(index=True, default=_get_default_category_code)    
    recovery_name = fields.Char(compute='_compute_recovery_name')
    #code_references = fields.Char(readonly=True)
    is_virtual_product = fields.Boolean()
    groupement = fields.Integer(default=3)
    
    
    @api.constrains('code_reference')
    def _check_code_reference(self):
        for rec in self:
            article = self.env['product.category'].search([('code_reference','=',rec.code_reference), ('id','!=',rec.id)])
            if article:
                raise ValidationError(_("Code %s existe déjà" % rec.code_reference))
    
    
    @api.onchange("category_code", "parent_id.code_reference")
    def _onchange_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = '%s-%s' % (rec.parent_id.code_reference, rec.category_code)
            else:
                rec.code_reference = '%s' % (rec.category_code)
    
    @api.onchange("parent_id")
    def _onchange_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = str(rec.parent_id.code_reference) + str(rec.category_code)
            else:
                rec.code_reference = rec.category_code
                
    @api.onchange("category_code")
    def _onchange_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = str(rec.parent_id.code_reference) + str(rec.category_code)
            else:
                rec.code_reference = rec.category_code
    
    
    @api.depends("name", "parent_id")
    def _compute_recovery_name(self):
        for rec in self:
            if rec.parent_id.is_virtual_product is True:
                rec.is_virtual_product = rec.parent_id.is_virtual_product
            if rec.is_virtual_product is True:
                rec.recovery_name = str(rec.parent_id.recovery_name) +' '+ str(rec.name)            
            else:
                rec.recovery_name = rec.name
                
                
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
    
#     @api.onchange("code_reference")
#     def _onchange_code_references(self):
#         for rec in self:
#             rec.resultat = rec.fonctionTranche(str(rec.code_reference),rec.groupement)
#             rec.code_references = rec.resultat
    