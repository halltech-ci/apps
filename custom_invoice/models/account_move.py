# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"
    
    delivery_slip=fields.Char(string='N° Bordereau de Livraison')
    customer_reference=fields.Char(string='Ref. Commande Client')
    signataire_facture=fields.Many2one('res.users', string='Signataire')
    invoice_object=fields.Char(string='Objet :')
    source_document=fields.Char(string='N° Bon de commande :')
    
    def function_create_invoice(self):
        pass
    