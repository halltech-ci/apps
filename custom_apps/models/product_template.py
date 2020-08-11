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

class ProductTemplate(models.Model):
    _inherit = "product.template"
    #Make default_code field mandatory
    def _get_sale_uom_id(self):
        return self.env["product.uom"].search([], limit=1, order='id').id
    
    type = fields.Selection(default='service')
    uom_so_id = fields.Many2one('product.uom', 'Sale Unit of Measure', default=_get_sale_uom_id, 
        help="Default Unit of Measure used for purchase orders. It must be in the same category than the default unit of measure.")