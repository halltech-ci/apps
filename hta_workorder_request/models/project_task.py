# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    product_lines = fields.One2many('product.request.line', 'task_id',string='Products',)
    stock_analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Move Analytic Account", help="Move created will be assigned to this analytic account",)
    stock_analytic_tag_ids = fields.Many2many(comodel_name="account.analytic.tag", string="Move Analytic Tags",)
    stock_analytic_line_ids = fields.One2many(comodel_name="account.analytic.line", inverse_name="stock_task_id", string="Analytic Lines",)