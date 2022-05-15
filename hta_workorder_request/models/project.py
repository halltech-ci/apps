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
