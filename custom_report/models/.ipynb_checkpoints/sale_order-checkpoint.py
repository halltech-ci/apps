# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    unite_de_mesure = fields.Selection(selection=[('achat', 'Achat'), ('vente', 'Vente')], string="Unite de mesure")