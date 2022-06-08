# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductRequestAllocation(models.Model):
    _name = "product.request.allocation"
    _description = 'Product request allocation'
    
    product_request_line_id = fields.Many2one('product.request.line', string="Product Request Line",
        required=True,
        ondelete="cascade",
        copy=True,
        index=True,
    )
    company_id = fields.Many2one("res.company", string="Company",
        readonly=True,
        related="product_request_line_id.request_id.company_id",
        store=True,
    )
    stock_move_id = fields.Many2one("stock.move", string="Stock Move",
        required=True,
        ondelete="cascade",
        index=True
    )
    product_id = fields.Many2one(string="Product", comodel_name="product.product",
        related="product_request_line_id.product_id",
        readonly=True,
    )
    product_uom_id = fields.Many2one(string="Unit",
        comodel_name="uom.uom",
        related="product_request_line_id.product_uom_id",
        readonly=True,
        required=True,
    )
    requested_product_uom_qty = fields.Float(
        "Requested Quantity (UoM)",
        help="Quantity of the stock request allocated to the stock move, "
        "in the UoM of the Stock Request",
    )
    requested_product_qty = fields.Float(
        "Requested Quantity",
        help="Quantity of the product allocated to the stock move, "
        "in the default UoM of the product",
    )
    allocated_product_qty = fields.Float(
        "Allocated Quantity",
        help="Quantity of the product allocated to the stock move, "
        "in the default UoM of the product",
    )
    open_product_qty = fields.Float(
        "Open Quantity", compute="_compute_open_product_qty"
    )
    request_state = fields.Selection(related="product_request_line_id.request_state")
    
    
    def _compute_open_product_qty(self):
        for rec in self:
            if rec.request_state in ["cancel", "done"]:
                rec.open_product_qty = 0.0
            else:
                rec.open_product_qty = (
                    rec.requested_product_uom_qty - rec.allocated_product_qty
                )
                if rec.open_product_qty < 0.0:
                    rec.open_product_qty = 0.0