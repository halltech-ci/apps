# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError

REQUEST_STATE = [('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('to_approve', 'To Approve'),
       ("open", "In progress"),
        ('done', 'Done'),
        ('close', 'Closed'),
        ('cancel', 'Refused')
        ]

class ProductRequestLine(models.Model):
    _name = "product.request.line"
    _description = "product line for product request"
    
    name = fields.Char(string="Description")
    request_state = fields.Selection(selection=REQUEST_STATE, string='Status', readonly=True, copy=False, default='draft', required=True, help='Expense Report State', related="request_id.state",)
    request_id = fields.Many2one('product.request', string="Product Request")
    product_id = fields.Many2one("product.product", string="Product", domain=[("purchase_ok", "=", True)], track_visibility="onchange",)
    product_uom_id = fields.Many2one("uom.uom", string="Product Unit of Measure", track_visibility="onchange", related='product_id.uom_id')
    requested_by = fields.Many2one("res.users", related="request_id.requested_by", string="Requested by", store=True,)
    initial_qty = fields.Float('Initial Qty', digits="Product Unit of Measure")#Quantity in sale order
    product_uom_qty = fields.Float('Product Qty', digits="Product Unit of Measure")#Quantity as for workorder
    qty_done = fields.Float('Qty Done', digits="Product Unit of Measure", compute='_compute_qty_done',)#Quantity give by stock
    product_request_allocation_ids = fields.One2many("product.request.allocation", "product_request_line_id", string="Product Request Allocation",)
    qty_in_progress = fields.Float(string="Qty In Progress", digits="Product Unit of Measure", readonly=True, store=True,
        help="Quantity in progress. Qty left", default=0)
    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account", track_visibility="onchange",)
    product_request_allocation_ids = fields.One2many("product.request.allocation", "product_request_line_id", string="Product Request Allocation",)
    task_id = fields.Many2one('project.task', string='Project Task', required=True, ondelete='cascade')
    project_id = fields.Many2one('project.project', related="request_id.project_id")
    #manage product_requestpicking
    move_ids = fields.One2many('stock.move', 'product_line_id', string='Reservation', readonly=True, ondelete='set null', copy=False)
    analytic_line = fields.Many2one('account.analytic.line', string="Analytic line")
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
    
    def _compute_qty(self):
        for line in self:
            line.qty_in_progess = 0
    
    def _create_stock_moves(self, picking):
        values = []
        for line in self:
            for val in line._prepare_stock_moves(picking):
                values.append(val)
        return self.env['stock.move'].create(values)
    
    def _create_stock_move_line(self, picking):
        values = []
        for line in self:
            for val in line._prepare_stock_moves(picking):
                values.append(val)
        return self.env['stock.move'].create(values)
           
    def action_to_approve(self):
        self.request_state = "to_approve"
    
    def action_approve(self):
        self.request_state = "open"
    
    def action_done(self):
        self.request_state = "done"
    
    def set_to_draft(self):
        self.request_state = 'draft'
        
    def action_close(self):
        self.request_state = 'close'
        
    def _get_stock_move_price_unit(self):
        self.ensure_one()
        line = self[0]
        price_unit = line.product_id.standard_price
        return price_unit