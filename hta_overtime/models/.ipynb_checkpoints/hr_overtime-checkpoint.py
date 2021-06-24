# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.base.models.res_partner import _tz_get

class HtaOvertime(models.Model):
    _name = 'hta.hr.overtime'
    _description = 'Custom overtime management'
    #_order = "date_from desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _mail_post_access = 'read'
    
    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env.user.employee_id
    
    def _employee_id_domain(self):
        if self.user_has_groups('hta_overtime.group_hr_overtime_user') or self.user_has_groups('hta_overtime.group_hr_overtime_manager'):
            return []
        if self.user_has_groups('hta_overtime.group_hr_overtime_responsible'):
            return [('overtime_manager_id', '=', self.env.user.id)]
        return [('user_id', '=', self.env.user.id)]

    name = fields.Char('Description')
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),  # YTI This state seems to be unused. To remove
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate1', 'Second Approval'),
        ('validate', 'Approved')
        ], string='Status', readonly=True, tracking=True, copy=False, default='draft',
        help="The status is set to 'To Submit', when a overtime request is created." +
        "\nThe status is 'To Approve', when overtime request is confirmed by user." +
        "\nThe status is 'Refused', when overtime request is refused by manager." +
        "\nThe status is 'Approved', when overtime request is approved by manager.")
    payslip_status = fields.Boolean('Reported in last payslips', help='Green this button when the overtime has been taken into account in the payslip.', copy=False)
    report_note = fields.Text('HR Comments', copy=False, groups="hta_overtime.group_hr_overtime_manager")
    user_id = fields.Many2one('res.users', string='User', related='employee_id.user_id', related_sudo=True, compute_sudo=True, store=True, default=lambda self: self.env.uid, readonly=True)
    manager_id = fields.Many2one('hr.employee')
    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True, ondelete="restrict",
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, default=_default_employee, tracking=True, domain=_employee_id_domain)
    # duration
    date_from = fields.Datetime('Start Date', readonly=True, index=True, copy=False, required=True,
        default=fields.Datetime.now,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, tracking=True)
    date_to = fields.Datetime('End Date', readonly=True, copy=False, required=True,
        default=fields.Datetime.now,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, tracking=True)
    #tz_mismatch = fields.Boolean(compute='_compute_tz_mismatch')
    tz = fields.Selection(_tz_get, compute='_compute_tz')
    department_id = fields.Many2one('hr.department', string='Department', readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    notes = fields.Text('Reasons', readonly=True, states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]})
    overtime_status_id = fields.Many2one(
        "hta.hr.overtime.type", string="Overtime Type", required=True, readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
        domain=[('valid', '=', True)])
    validation_type = fields.Selection('Validation Type', related='overtime_status_id.validation_type', readonly=False)
    first_approver_id = fields.Many2one('hr.employee', string='First Approval', readonly=True, copy=False,
        help='This area is automatically filled by the user who validate the overtime')
    second_approver_id = fields.Many2one(
        'hr.employee', string='Second Approval', readonly=True, copy=False,
        help='This area is automatically filled by the user who validate the time off with second level (If overtime type need second validation)')

    
    """
    @api.depends('tz')
    def _compute_tz_mismatch(self):
        for overtime in self:
            overtime.tz_mismatch = overtime.tz != self.env.user.tz
    """

    @api.depends('employee_id')
    def _compute_tz(self):
        for overtime in self:
            tz = overtime.employee_id.tz
    
    def action_confirm(self):
        if self.filtered(lambda overtime: overtime.state != 'draft'):
            raise UserError(_('overtime request must be in Draft state ("To Submit") in order to confirm it.'))
        self.write({'state': 'confirm'})
        overtimes = self.filtered(lambda overtime: overtime.validation_type == 'no_validation')
        if overtimes:
            # Automatic validation should be done in sudo, because user might not have the rights to do it by himself
            overtimes.sudo().action_validate()
        self.activity_update()
        return True

    def action_approve(self):
        # if validation_type == 'both': this method is the first approval approval
        # if validation_type != 'both': this method calls action_validate() below
        if any(overtime.state != 'confirm' for overtime in self):
            raise UserError(_('Overtime request must be confirmed ("To Approve") in order to approve it.'))

        current_employee = self.env.user.employee_id
        self.filtered(lambda ove: ove.validation_type == 'both').write({'state': 'validate1', 'first_approver_id': current_employee.id})


        # Post a second message, more verbose than the tracking message
        for overtime in self.filtered(lambda overtime: overtime.employee_id.user_id):
            overtime.message_post(
                body=_('Your %s planned on %s has been accepted') % (overtime.holiday_status_id.display_name, overtime.date_from),
                partner_ids=overtime.employee_id.user_id.partner_id.ids)

        self.filtered(lambda ove: not ove.validation_type == 'both').action_validate()
        if not self.env.context.get('leave_fast_create'):
            self.activity_update()
        return True
