# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    @api.model
    def _default_picking_type(self):
        return self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
    
    src_location = fields.Many2one('stock.location', string="Emplacement source", readonly=False, index=True, check_company=True)
    dest_location = fields.Many2one('stock.location', string="Emplacement destination", readonly=False, index=True, check_company=True)
    picking_type = fields.Many2one('stock.picking.type', string='Opération', readonly=False, index=True, check_company=True, default=_default_picking_type)
    
    @api.onchange("picking_type")
    def onchange_picking_type(self):
        self.src_location = self.picking_type.default_location_src_id.id
        self.dest_location = self.picking_type.default_location_dest_id.id

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    product_lines = fields.One2many('product.request.line', 'task_id',string='Products',)
    stock_analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Move Analytic Account", help="Move created will be assigned to this analytic account",)
    stock_analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Move Analytic Tags",)
    stock_analytic_line_ids = fields.One2many(comodel_name="account.analytic.line", inverse_name="stock_task_id", string="Analytic Lines",)