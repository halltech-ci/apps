# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""Ressource calendar is working plan. A working plan contain attendance (working hours), leaves and overtimes.
    by default attendance and leaves are integrated in Odoo. This module is build to add overtime in calendar ressource
"""

class RessourceCalendar(models.Model):
    _inherit = "resource.calendar"
    
    overtime_ids = fields.One2many(
        'resource.calendar.overtime', 'calendar_id', 'Overtime', copy=True)
    
class RessourceCalendarOvertime(models.Model):
    _name = "resource.calendar.overtime"
    _description = "Resource overtime Detail"
    _order = "date_from"

    name = fields.Char('Reason')
    company_id = fields.Many2one(
        'res.company', related='calendar_id.company_id', string="Company",
        readonly=True, store=True)
    calendar_id = fields.Many2one('resource.calendar', 'Working Hours')
    date_from = fields.Datetime('Start Date', required=True)
    date_to = fields.Datetime('End Date', required=True)
    resource_id = fields.Many2one(
        "resource.resource", 'Resource',
        help="If empty, this is a generic overtime for the company. If a resource is set, the overtime is only for this resource")
    to_approve = fields.Boolean(default=True,
                                 help="Whether this should be approve before taking account in payslip")
    
    
class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'
    
    day_period = fields.Selection(selection_add=[('night', 'Nigth')])
