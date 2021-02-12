# -*- coding: utf-8 -*-

from odoo import models, fields, api

REQUEST_STATES = [
    ("draft", "Draft"),
    ("open", "In progress"),
    ("done", "Done"),
    ("cancel", "Cancelled"),
]

class ProductRequest(models.Model):
    _name ="product.request"
    _description = "Product request"
    
    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)
    
    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.request")
    
    name = fields.Char(string="Request Reference",
        required=True,
        default=_get_default_name,
        track_visibility="onchange",
    )
    company_id = fields.Many2one("res.company", "Company",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.company,
    ) 
    state = fields.Selection(
        selection=REQUEST_STATES,
        string="Status",
        copy=False,
        default="draft",
        index=True,
        readonly=True,
        track_visibility="onchange",
    )
    date = fields.Datetime(readonly=True, default=fields.Datetime.now, string="Date")
    line_ids = fields.One2many(
        comodel_name="product.request.line",
        inverse_name="request_id",
        string="Products to request",
        readonly=False,
        copy=True,
        track_visibility="onchange",
    )
    requested_by = fields.Many2one("res.users",
        string="Requested by",
        required=True,
        copy=False,
        track_visibility="onchange",
        default=_get_default_requested_by,
        index=True,
    )
    project_task_id = fields.Many2one('project.task', string="Project Task")
    project_id = fields.Many2one('project.project', string="Project")
    analytic_account_id = fields.Many2one("account.analytic.account",
        string="Analytic Account",
        track_visibility="onchange",
    )
    
    
    @api.model
    def create(self, vals):
        request = super(ProductRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(ProductRequest, self).write(vals)
        return res
    
    
    

    
    