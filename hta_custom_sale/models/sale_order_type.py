# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderTypology(models.Model):
    _name = "sale.order.type"
    _description = "Type of sale order"

    @api.model
    def _get_domain_sequence_id(self):
        seq_type = self.env.ref("sale.seq_sale_order")
        return [("code", "=", seq_type.code)]

    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    sequence_id = fields.Many2one(comodel_name="ir.sequence", string="Entry Sequence", copy=False, domain=_get_domain_sequence_id,)
