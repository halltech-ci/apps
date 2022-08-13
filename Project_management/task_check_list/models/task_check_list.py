# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    #task_checklist = fields.Many2many('task.checklist', string='Check List')
    checklist_progress = fields.Float(compute="_compute_checklist_progress", string='Check list Progress', store=True, recompute=True, default=0.0, group_operator="avg")
    max_rate = fields.Integer(string='Maximum rate', compute="_compute_max_rate")
    check_list_ids = fields.One2many('task.checklist', "task_id", string="Check list")
    task_status = fields.Boolean(string="Status", default=False)
    
    
    @api.depends('check_list_ids')
    def _compute_max_rate(self):
        max_rate = 0
        for list in self.check_list_ids:
            max_rate += list.unit_time
        self.max_rate = max_rate
        
    @api.depends("check_list_ids.unit_time", "max_rate")
    def _compute_checklist_progress(self):
        for rec in self:
            total_check = 0
            for line in rec.check_list_ids:
                if line.check_box == True:
                    total_check += line.unit_time
            if rec.max_rate != 0:
                rec.checklist_progress = 100 * total_check/rec.max_rate
            else:
                rec.checklist_progress = 0
                
    @api.onchange("checklist_progress")
    def _onchange_checklist_progess(self):
        for task in self:
            if task.checklist_progress == 100.0:
                task.task_status = True
            else:
                task.checklist_progress = False
                #task.subtask_effective_hours = sum(child_task.effective_hours + child_task.subtask_effective_hours for child_task in task.child_ids)
        
class TaskChecklist(models.Model):
    _name = 'task.checklist'
    _description = 'Checklist for the task'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    task_id = fields.Many2one("project.task")
    #employee_id = fields.Many2one('hr.employee')
    check_box = fields.Boolean(default=False)
    unit_time = fields.Float(string="Duration", default=0, requied=True)
    date = fields.Date(default=fields.Datetime.now().date())
    
