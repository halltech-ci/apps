# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit="project.project"
    
    sale_order_ids = fields.Many2many("sale.order", string="Sale Order", copy=False, compute="_compute_sale_order_ids")
    
    @api.depends('sale_order_id')
    def _compute_sale_order_ids(self):
        for rec in self:
            sales = rec.mapped('sale_order_id')
            rec.sale_order_ids = sales
