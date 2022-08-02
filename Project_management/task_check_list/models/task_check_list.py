# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    
    @api.depends('check_list_ids.unit_time')
    def checklist_progress(self):
        """:return the value for the check list progress"""
        for rec in self:
            total_check = sum(rec.check_list_ids.filtered(lambda l:l.check_box == True).unit_time)
        if self.max_rate != 0:
            rec.checklist_progress = total_check / max_rate
        else:
            rec.checklist_progress = 0

    #task_checklist = fields.Many2many('task.checklist', string='Check List')
    checklist_progress = fields.Float(compute=checklist_progress, string='Check list Progress', store=True, recompute=True, default=0.0)
    max_rate = fields.Integer(string='Maximum rate', compute="_compute_max_rate")
    check_list_ids = fields.One2many('task.checklist', "task_id", string="Check list")
    
    
    @api.depends('check_list_ids')
    def _compute_max_rate(self):
        max_rate = 0
        for list in self.check_list_ids:
            max_rate += list.unit_time
        self.max_rate = max_rate
        


class TaskChecklist(models.Model):
    _name = 'task.checklist'
    _description = 'Checklist for the task'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    task_id = fields.Many2one("project.task")
    employee_id = fields.Many2one('hr.employee')
    check_box = fields.Boolean(default=False)
    unit_time = fields.Float(string="Duration", default=0, requied=True)
    
