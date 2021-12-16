#from odoo import models, fields, api, _



class CodeCategorie(models.Model):
    _inherit = 'product.category'
    

    category_code = fields.Char()
    code_reference = fields.Char()    
    recovery_name = fields.Char(compute='_compute_recovery_name')
    is_virtual_product = fields.Boolean()
    groupement = fields.Integer(default=3)
    code_range = fields.Selection([('1', '1 Chiffre'),
                                  ('2', '2 Chiffres'),
                                  ('3', '3 Chiffres')], default='3')
    
    
    @api.onchange("category_code", "parent_id.code_reference")
    def _onchange_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = '%s-%s' % (rec.parent_id.code_reference, rec.category_code)
            if rec.category_code:
                rec.code_reference = '%s' % (rec.category_code)
            else:
                rec.code_reference = rec.code_reference
    
    @api.onchange("parent_id")
    def _onchange_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = str(rec.parent_id.code_reference) + str(rec.category_code)
            if rec.category_code:
                rec.code_reference = '%s' % (rec.category_code)
            else:
                rec.code_reference = rec.code_reference

                
    @api.onchange("category_code")
    def _onchange_code_reference(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_reference = str(rec.parent_id.code_reference) + str(rec.category_code)
            if rec.category_code:
                rec.code_reference = '%s' % (rec.category_code)
            else:
                rec.code_reference = rec.code_reference
    
    
    @api.depends("name", "parent_id")
    def _compute_recovery_name(self):
        for rec in self:
            if rec.parent_id.is_virtual_product is True:
                rec.is_virtual_product = rec.parent_id.is_virtual_product
            if rec.is_virtual_product is True:
                rec.recovery_name = str(rec.parent_id.recovery_name) +' '+ str(rec.name)            
            else:
                rec.recovery_name = rec.name
                