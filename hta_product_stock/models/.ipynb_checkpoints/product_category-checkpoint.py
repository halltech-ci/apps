# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HtaCategory(models.Model):
    _inherit = 'product.category'
    

    category_code = fields.Char() # Code Category
    code_concate = fields.Char(compute='_compute_code_concate') # Concate all code
    template_code = fields.One2many('product.template', 'categ_id', 'Code Template')
    recovery_name = fields.Char(compute='_compute_recovery_name')
    type_category_ids = fields.Many2many('product.category.type')
    is_virtual_product = fields.Boolean()
    code_range = fields.Selection([('1', '1 Chiffre'),
                                  ('2', '2 Chiffres'),
                                  ('3', '3 Chiffres')], default='3')
    
    
    @api.depends("name", "parent_id")
    def _compute_recovery_name(self):
        for rec in self:
            if rec.parent_id.is_virtual_product is True:
                rec.is_virtual_product = rec.parent_id.is_virtual_product
            if rec.is_virtual_product is True:
                rec.recovery_name = str(rec.parent_id.recovery_name) +' '+ str(rec.name)            
            else:
                rec.recovery_name = rec.name
    
    @api.onchange("parent_id")
    def _compute_code_concate(self):
        for rec in self:
            if rec.parent_id: 
                rec.code_concate = str(rec.parent_id.code_concate) + str(rec.category_code)
            else:
                rec.code_concate = rec.category_code


class ProductCategoryType(models.Model):
    _name = 'product.category.type'
    _description = 'Product Type Category'
    #_inherit = ['mail.thread','mail.activity.mixin']
    
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")