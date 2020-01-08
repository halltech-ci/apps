# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class custom_apps(models.Model):
#     _name = 'custom_apps.custom_apps'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Project(models.Model):
    _inherit = "project.project"
    
    purchase_order_ids = fields.One2many("purchase.order", 
                                         "project_id", 
                                         string="Purchase Order"
    )
    project_code = fields.Char(string='Code Projet', required=True, readonly=True, default='Nouveau', copy=False)
    
    '''
    @api.model
    def create
    '''