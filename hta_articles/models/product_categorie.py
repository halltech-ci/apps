from odoo import models, fields, api, _


class CodeCategorie(models.Model):
    _inherit = 'product.category'

    code = fields.Char()
    _sql_constraints = [('code_unique', 'unique (code)', "This code already exists!")]
    
    l_name = fields.Char(compute='_compute_l_name')
    #code_reference = fields.Char()
    code_reference = fields.Char(compute='_compute_code_reference')
    is_virtual_product = fields.Boolean()
    
    
    
    @api.onchange("code","parent_id")
    def _compute_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = rec.parent_id.code
            else:
                rec.code_reference = rec.code
                
    
    @api.depends("name", "parent_id")
    def _compute_l_name(self):
        for rec in self:
            if rec.parent_id.is_virtual_product is True:
                rec.is_virtual_product = rec.parent_id.is_virtual_product
            if rec.is_virtual_product is True:
                rec.l_name = str(rec.parent_id.l_name) +' '+ str(rec.name)            
            else:
                rec.l_name = rec.name
                
                
               
            
                
                
    
    @api.onchange("parent_id")
    def _compute_code_categorie(self):
        for rec in self:
            if rec.parent_id:
                rec.code = rec.parent_id.code