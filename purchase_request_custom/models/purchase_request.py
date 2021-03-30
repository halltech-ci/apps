# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _inherit = "purchase.request"
    
    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.da.sequence")
    
    @api.depends('requested_by')
    def _compute_has_manager(self):
        for rec in self:
            if rec.requested_by:
                employee = self.env['hr.employee'].search([('work_email', '=', rec.requested_by.email)], limit = 1)
                if (employee.department_id) and (employee.department_id.manager_id):
                    rec.has_manager = True
                else:
                    rec.has_manager = False
                    
    sale_order = fields.Many2one('sale.order', string='Sale Order')
    project = fields.Many2one('project.project' ,related='sale_order.project_id', string="Project", readonly=True)
    project_code = fields.Char(related='project.code', string="Project Code", readonly=True)
    purchase_type = fields.Selection(selection=[('project', 'Projet'), ('autres', 'Autres')], string="Request Type")
    #has_manager = fields.Boolean(compute='_compute_has_manager')
    is_project_approver = fields.Boolean(compute='_compute_is_project_approver')
    is_expense = fields.Boolean('is_expense', default=False)
    
    """
    def action_send_email(self):
        #self.ensure_one()
        template_id = self.env.ref('purchase_request.email_template_purchase_request').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
    """
    #@api.depends('')
    def _compute_is_project_approver(self):
        for req in self:
            user = self.env.user
            if user.has_group('project.group_project_manager'):
                req.is_project_approver = True
            else:
                req.is_project_approver = False
    
    @api.model
    def create(self, vals):
        request = super(PurchaseRequest, self).create(vals)
        if vals.get("assigned_to"):
            partner_id = self._get_partner_id(request)
            request.message_subscribe(partner_ids=[partner_id])
            #self.action_send_email()
        return request
    
    def to_approve_check(self):
        user = self.env.user
        if not user.has_group('purchase_request_custom.group_purchase_request_approver'):
            raise UserError(
                    _("You are not allow to approve this request.")
                )
    
    def button_approved(self):
        self.to_approve_check()
        if self.project and not self.is_project_approver:
            raise UserError(
                    _("You are not allow to approve this request.")
                )
        return self.write({"state": "approved"})
    
class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"
    
    project = fields.Many2one(related="request_id.project", string="Project", readonly=True)
    product_code = fields.Char(related="product_id.default_code", sting="Code Article")