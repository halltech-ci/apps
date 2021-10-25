from odoo import models, fields, api, _


class CodeCategorie(models.Model):
    _inherit = 'product.category'

    code = fields.Char()
    _sql_constraints = [('code_unique', 'unique (code)', "This code already exists!")]
    
    recovery_name = fields.Char(compute='_compute_recovery_name')
    #code_reference = fields.Char()
    code_reference = fields.Char(compute='_compute_code_reference')
    code_reference2 = fields.Char()
    is_virtual_product = fields.Boolean()
    
    
    
    @api.onchange("code","parent_id")
    def _compute_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = str(rec.parent_id.code_reference) + str(rec.code)
            else:
                rec.code_reference = rec.code
                
    
    @api.depends("name", "parent_id")
    def _compute_recovery_name(self):
        for rec in self:
            if rec.parent_id.is_virtual_product is True:
                rec.is_virtual_product = rec.parent_id.is_virtual_product
            if rec.is_virtual_product is True:
                rec.recovery_name = str(rec.parent_id.recovery_name) +' '+ str(rec.name)            
            else:
                rec.recovery_name = rec.name
                