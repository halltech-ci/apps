# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    product_lines = fields.One2many('product.request.line', 'task_id',string='Products',
                                   compute="_compute_product_lines",
    )
    
    def _compute_product_lines(self):
        for rec in self:
            rec.product_lines = self.env['product.request'].search([('project_task_id', '=', rec.id)]).mapped('line_ids')
    
    def button_action_product(self):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Product Request',
                'target': 'new', #use 'current' for not opening in a dialog
                'res_model': 'product.request',
                'res_id': self.env['product.request'].search([('project_task_id', '=', self.id)]).id,
                #'view_id': 'view_xml_id',#optional
                'view_type': 'form',
                'views': [[False,'form']],
                'context': {#your context
                        'project_task_id': self.id,
                        },
                };