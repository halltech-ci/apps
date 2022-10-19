# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order.item"
    
    keep_description = fields.Boolean(
        string="Copy descriptions to new PO",
        help="Set true if you want to keep the "
        "descriptions provided in the "
        "wizard in the new PO.", default=True
    )