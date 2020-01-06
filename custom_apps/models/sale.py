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

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    project_id = fields.Many2one("project.project", "Project", ondelete= "set null")
    purchase_order_subject = fields.Text("Objet : ")
    signed_user = fields.Many2one("res.users", string="Signed In User", readonly=True, default= lambda self: self.env.uid)
    '''
    @api.multi
    def get_signed_user(self):
        return self.env.user
    '''
    