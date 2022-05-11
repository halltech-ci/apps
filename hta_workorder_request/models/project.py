# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    src_location = fields.Many2one('stock.location', string="Emplacement source", readonly=False, index=True, check_company=True)
    dest_location = fields.Many2one('stock.location', string="Emplacement destination", readonly=False, index=True, check_company=True)
    picking_type = fields.Many2one('stock.picking.type', string='Opération', readonly=False, index=True, check_company=True)
    
    @api.onchange("picking_type_id")
    def onchange_picking_type(self):
        self.location_id = self.picking_type_id.default_location_src_id.id
        self.location_dest_id = self.picking_type_id.default_location_dest_id.id

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    product_lines = fields.One2many('product.request.line', 'task_id',string='Products',)
    stock_analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Move Analytic Account", help="Move created will be assigned to this analytic account",)
    stock_analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Move Analytic Tags",)
    stock_analytic_line_ids = fields.One2many(comodel_name="account.analytic.line", inverse_name="stock_task_id", string="Analytic Lines",)