# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

REQUEST_STATE = [('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('to_approve', 'To Approve'),
       ("open", "In progress"),
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
        related='product_id.uom_id'
    )
    requested_by = fields.Many2one("res.users",
        related="request_id.requested_by",
        string="Requested by",
        store=True,
    )
    initial_qty = fields.Float('Initial Qty', digits="Product Unit of Measure")
    product_uom_qty = fields.Float('Product Qty', digits="Product Unit of Measure")
    qty_done = fields.Float('Qty Done', digits="Product Unit of Measure",
        compute='_compute_qty_done',
    )
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
    display_type = fields.Selection([('line_section', "Section"), ('line_note', "Note")], 
        default=False, help="Technical field for UX purpose.")
    #manage product_requestpicking
    move_ids = fields.One2many('stock.move', 'product_line_id', string='Reservation', readonly=True, ondelete='set null', copy=False)
    #move_dest_ids = fields.One2many('stock.move', 'created_product_request_line_id', 'Downstream Moves')
    
    @api.constrains('initial_qty', 'product_uom_qty')
    def compare_product_qty(self):
        for line in self:
            if line.initial_qty > 0 and line.product_uom_qty > 0:
                if self.initial_qty < self.product_uom_qty:
                    raise ValidationError(_("{0} quantity can not be greater than {1}".format(self.product_id.name, self.initial_qty)))
    
    @api.depends('move_ids')
    def _compute_qty_done(self):
        for line in self:
            qty = 0
            if len(line.move_ids) > 0:
                for move in line.move_ids:
                    qty += move.quantity_done
            line.qty_done = qty
           
    def action_to_approve(self):
        self.request_state = "to_approve"
    
    def action_approve(self):
        self.request_state = "open"
    
    def action_done(self):
        self.request_state = "done"
    
    def _get_stock_move_price_unit(self):
        self.ensure_one()
        line = self[0]
        price_unit = line.product_id.standard_price
        return price_unit
    
    