# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequestLine(models.Model):
    _inherit = ["purchase.request.line", "product.configurator"]
    _name = "purchase.request.line"
