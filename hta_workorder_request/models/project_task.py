# -*- coding: utf-8 -*-

from odoo import models, fields, api

STATES = [('open', 'Opened'),
         ('done', 'Done'),
         ('close', 'Closed')
         ]

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    product_lines = fields.One2many('product.request.line', 'task_id', string='Products',)
    use_product = fields.Boolean('Consomme stock')
    stock_move_ids = fields.One2many('stock.move', compute='_compute_stock_move_ids', string='Stock Moves')
    state = fields.Selection(selection=STATES, default='open')
    
    def _action_close_task(self):
        pass
    #adding stoc_move_ids in project_task
    @api.depends('product_lines.move_ids')
    def _compute_stock_move_ids(self):
        for task in self:
            task.stock_move_ids = task.mapped('product_lines.move_ids')
    
class projectTaskType(models.Model):
    _inherit = 'project.task.type'
    
    closed = fields.Boolean(help="project task closed state")
