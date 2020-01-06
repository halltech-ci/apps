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

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    proforma_invoice = fields.Char(string="N° Devis/Proforma", store=True)
    total_amount_letter = fields.Text(string="Montant total en lettre:")
    project_id = fields.Many2one("project.project", "Project", ondelete="set null")
    

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    item = fields.Integer(string="Item", store=False)
    date_planned = fields.Datetime(string='Scheduled Date', required=False, index=True)