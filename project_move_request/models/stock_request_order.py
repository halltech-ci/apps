# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"
    
    project_task = fields.Many2one('project.task')
    timesheet_ids = fields.One2many(related="project_task.timesheet_ids")
    equipment_ids = fields.One2many('maintenance.equipment', 'request_order', string="Equipement")
    
    
    #@api.constrains()
    
    @api.model
    def create(self, vals):
        upd_vals = vals.copy()
        if upd_vals.get("name", "/") == "/":
            upd_vals["name"] = self.env["ir.sequence"].next_by_code(
                "work.order.request"
            )
        return super().create(upd_vals)