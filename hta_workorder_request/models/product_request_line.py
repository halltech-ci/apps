# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

REQUEST_STATE = [('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('to_approve', 'To Approve'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Refused')
        ]


class ProductRequestLine(models.Model):
    _name = "product.request.line"
    _description = "product line for product request"
    
    name = fields.Char(string="Description")
    request_state = fields.Selection(selection=REQUEST_STATE, string='Status', readonly=True, 
                    copy=False, 
                    default='draft', 
                    required=True,
                    help='Expense Report State',
                    related="request_id.state",
    )
    request_id = fields.Many2one('product.request', string="Product Request")
    product_id = fields.Many2one("product.product", string="Product",
        domain=[("sale_ok", "=", True)],
        track_visibility="onchange",
    )
    product_uom_id = fields.Many2one("uom.uom",
        string="Product Unit of Measure",
        track_visibility="onchange",
    )
    requested_by = fields.Many2one("res.users",
        related="request_id.requested_by",
        string="Requested by",
        store=True,
    )
    initial_qty = fields.Float('Initial Qty', digits="Product Unit of Measure")
    product_qty = fields.Float('Product Qty', digits="Product Unit of Measure")
    qty_reserved = fields.Float('Used Qty', digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty",
        store=True,
        help="Quantity in progress.",)
    qty_done = fields.Float('Qty Done', digits="Product Unit of Measure")
    product_request_allocation_ids = fields.One2many("product.request.allocation",
        "product_request_line_id",
        string="Product Request Allocation",
    )
    qty_in_progress = fields.Float(string="Qty In Progress", digits="Product Unit of Measure",
        readonly=True,
        compute="_compute_qty",
        store=True,
        help="Quantity in progress. Qty left",
    )
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account",
        string="Analytic Account",
        track_visibility="onchange",
    )
    product_request_allocation_ids = fields.One2many("product.request.allocation",
        "product_request_line_id",
        string="Product Request Allocation",
    )
    task_id = fields.Many2one('project.task', string='Project Task')
    project_id = fields.Many2one('project.project', related="request_id.project_id")
    
    
    @api.constrains('initial_qty', 'product_qty')
    def compare_product_qty(self):
        if self.initial_qty > 0 and self.product_qty > 0:
            if self.initial_qty < self.product_qty:
                raise ValidationError(_("{0} quantity can not be greater than {1}".format(self.product_id.name, self.initial_qty)))
    
    @api.depends('product_request_allocation_ids',)
    def _compute_qty(self):
        for request in self:
            done_qty = sum(
                request.product_request_allocation_ids.mapped("allocated_product_qty")
            )
            open_qty = sum(
                request.product_request_allocation_ids.mapped("open_product_qty")
            )
            request.qty_done = done_qty
            request.qty_in_progress = open_qty
            
    def action_to_approve(self):
        self.request_state = "to_approve"
    
    def action_approve(self):
        self.request_state = "open"
    
    