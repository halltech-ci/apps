# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    product_lines = fields.One2many('product.request.line', 'task_id',string='Products',)
    stock_analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Move Analytic Account", help="Move created will be assigned to this analytic account",)
    stock_analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Move Analytic Tags",)
    stock_analytic_line_ids = fields.One2many(comodel_name="account.analytic.line", inverse_name="stock_task_id", string="Analytic Lines",)
    move_ids = fields.One2many('stock.move', 'product_request', string = "Stock Move", copy=False, domain = [('scrapped', '=', False)])
    picking_type_id = fields.Many2one('stock.picking.type', related='project_id.picking_type')
    location_id = fields.Many2one("stock.location", string="Source Location", related="project_id.src_location", readonly=False, index=True, check_company=True,)
    location_dest_id = fields.Many2one("stock.location", related="project_id.dest_location", string="Destination Location", readonly=False, index=True, check_company=True,)
    
    def action_done(self):
        for move in self.mapped("move_ids"):
            move.quantity_done = move.reserved_availability
        self.mapped("move_ids")._action_done()
        analytic_line_model = self.env["account.analytic.line"]
        for move in self.move_ids.filtered(lambda x: x.state == "done"):
            vals = move._prepare_analytic_line_from_task()
            if vals:
                analytic_line_model.create(move._prepare_analytic_line_from_task())