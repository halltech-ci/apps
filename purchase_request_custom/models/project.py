# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = "project.project"
    
    purchase_line_ids = fields.One2many('purchase.order.line', compute="_compute_purchase_line_ids")
    
    #@api.depends('sale_order_id')
    def _compute_purchase_line_ids(self):
        for rec in self:
            lines = self.env['purchase.order.line'].search([('project_id', "=", rec.id)])#.mapped('sale_order_id')
            rec.sale_order_ids = lines
