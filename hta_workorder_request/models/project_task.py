# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    product_lines = fields.One2many('product.request.line', 'task_id',string='Products',)
    use_product = fields.Boolean('Consomme stock')
    
    def _action_close_task(self):
        pass
    
class projectTaskType(models.Model):
    _inherit = 'project.task.type'
    
    closed = fields.Boolean(help="project task closed state")
