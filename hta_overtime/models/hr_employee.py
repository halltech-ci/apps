# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'
    
    overtime_manager_id = fields.Many2one(
        'res.users', string='Overtime',
        help="User responsible of overtime approval.")