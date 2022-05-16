# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.scrap"

    product_request = fields.Many2one("product.request", string="Task", check_company=True)
    task_id = fields.Many2one('project.task', related="product_request.project.task_id")

    @api.onchange("product_request")
    def _onchange_task_id(self):
        if self.task_id:
            self.location_id = self.task_id.move_ids.filtered(lambda x: x.state not in ("done", "cancel")) and (self.task_id.location_id.id or self.task_id.location_dest_id.id)

    def _prepare_move_values(self):
        vals = super()._prepare_move_values()
        if self.task_id:
            vals["origin"] = vals["origin"] or self.task_id.name
            vals.update({"product_request_task_id": self.task_id.id})
        return vals

    def _get_origin_moves(self):
        return super()._get_origin_moves() or (
            self.task_id
            and self.task_id.move_ids.filtered(
                lambda x: x.product_id == self.product_id
            )
        )