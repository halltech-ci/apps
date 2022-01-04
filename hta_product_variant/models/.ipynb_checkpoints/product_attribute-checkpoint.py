# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"
    
    field_type = fields.Selection(selection=([('number', 'numeric'), ('char', 'alpha-numeric')]), string="Type de donnes")
    field_length = fields.Selection(selection=([('1', 'Un'), ('2', 'Deux'), ('3', 'Trois'), ('4', 'Quatre')]), string="Nombre de caracteres")