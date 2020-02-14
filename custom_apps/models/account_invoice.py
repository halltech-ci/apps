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


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    delivery_document=fields.Char(string='N° Bordereau de Livraison')
    customer_reference=fields.Char(string='Ref. Commande Client')
    signataire_facture=fields.Many2one('res.users', string='Signataire')
    invoice_object=fields.Char(string='Objet :')