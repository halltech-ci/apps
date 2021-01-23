# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    project_id = fields.Many2one('project.project', string='Project', readonly = True,
                                 default=lambda self: self._get_project_idenv['purchase.order.line'].search([('order_id', '=', self.id)], limit=1).project_id.key)
    
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    project_id = fields.Many2one('project.project', compute='_compute_project_id', string="Project")
    
    @api.depends('purchase_request_allocation_ids')
    def _compute_project_id(self):
        for rec in self:
            if rec.purchase_request_allocation_ids:
                allocation_ids = self.env['purchase.order.line'].search([], limit=1).mapped('purchase_request_allocation_ids')
                #allocation_ids = rec.mapped('purchase_request_allocation_ids') 
                #if len(allocation_ids) == 1:
                rec.project_id = allocation_ids.purchase_request_line_id.project or False