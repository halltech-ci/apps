# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    @api.model
    def _get_default_picking_type(self):
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        return self.env['stock.picking.type'].search([('code', '=', 'internal'), ('warehouse_id.company_id', '=', company_id), ], limit=1)
    
    @api.model
    def _get_default_location_src_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self.env.context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_src_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False

    @api.model
    def _get_default_location_dest_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self._context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_dest_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False
    
    picking_type = fields.Many2one('stock.picking.type', 'Picking Type', default=_get_default_picking_type, )
    location_src_id = fields.Many2one("stock.location", string="Emplacement Source", required=True, default=_get_default_location_src_id, domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    location_dest_id = fields.Many2one(string="Destination", comodel_name="stock.location", required=True, default=_get_default_location_dest_id, domain="[('usage','=','internal'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    
    
    def action_close_project(self):
        for project in self:
            tasks = project.mapped('tasks')
            for task in tasks:
                task._action_close_task()
        return True
    
    @api.onchange("picking_type")
    def onchange_picking_type(self):
        self.location_src_id = self.picking_type.default_location_src_id.id
        self.location_dest_id = self.picking_type.default_location_dest_id.id
