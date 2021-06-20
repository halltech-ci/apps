# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID, tools


class HrOvertime(models.Model):
    _name = "hr.overtimes"
    _description = "Hr Overtime"
    _order = "date_from desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'
    
    
    name = fields.Char('Description')
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
        ], string='Status', readonly=True, tracking=True, copy=False, default='draft',
        help="The status is set to 'To Submit', when a overtime request is created." +
        "\nThe status is 'To Approve', when overtime request is confirmed by user." +
        "\nThe status is 'Refused', when overtime request is refused by manager." +
        "\nThe status is 'Approved', when overtime request is approved by manager.")
    payslip_status = fields.Boolean('Reported in last payslips', copy=False, 
                        help='Green this button when the overtime has been taken into account in the payslip.', )
    report_note = fields.Text('HR Comments', copy=False, groups="hta_custom_overtime.group_hr_overtime_manager")
    """user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', related_sudo=True, compute_sudo=True, store=True, default=lambda self: self.env.uid, readonly=True)
    """
    manager_id = fields.Many2one('hr.employee')
    # leave type configuration
    overtime_status_id = fields.Many2one(
        "hr.overtimes.type", string="Time Off Type", required=True, readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
        domain=[('valid', '=', True)])
    #validation_type = fields.Selection('Validation Type', related='overtime_status_id.validation_type', readonly=False)
    

class HrOvertimeType(models.Model):
    _name = 'hr.overtimes.type'
    _description = "Overtime type"
    
    name = fields.Char()
    

    


