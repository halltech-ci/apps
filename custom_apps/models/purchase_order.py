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
    
    proforma_invoice = fields.Char(string="N° Devis Fournisseur :", store=True)
    total_amount_letter = fields.Text(string="Montant total en lettre:")
    #project_id = fields.Many2one("project.project", "Project", ondelete="cascade")
    sale_order_id = fields.Many2one("sale.order", "Sale Order", ondelete="cascade")
    
    #Overide create method to add custom sequence
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order.sequence') or '/'
        return super(PurchaseOrder, self).create(vals)
    
    
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    item = fields.Integer(string="Item", store=True)
    date_planned = fields.Datetime(string='Scheduled Date', required=False, index=True)
    product_code = fields.Char(string = "Product Code", 
                               related="product_id.default_code")
    product_name = fields.Char(string="Product Description", 
                           related="product_id.name")
    
    
