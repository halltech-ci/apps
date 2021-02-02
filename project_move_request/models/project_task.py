# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"
    
    stock_request_ids = fields.One2many('stock.request', 'task_id', string='Stock Request')
    
    def button_action_product(self):
        return {
                'type': 'ir.actions.act_window',
                'name': 'Stock Request',
                'target': 'new', #use 'current' for not opening in a dialog
                'res_model': 'stock.request.order',
                #'res_id': target_id,
                'view_id': 'view_xml_id',#optional
                'view_type': 'form',
                'views': [[False,'form']],
                'context': {#your context
                        'project_task': self.id,
                        },
                };