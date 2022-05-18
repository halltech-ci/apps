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
        domain=[("purchase_ok", "=", True)],
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
            
    def _prepare_stock_moves(self, picking):
        """ Prepare the stock moves data for one product line. This function returns a list of
        dictionary ready to be used in stock.move's create()
        """
        self.ensure_one()
        res = []
        if self.product_id.type not in ['product', 'consu']:
            return res
        qty = 0.0
        price_unit = self._get_stock_move_price_unit()
        moves = self.move_ids.filtered(lambda r: r.state != 'cancel' and not r.scrapped and self.product_id == r.product_id)
        for move in moves:
            qty -= move.product_uom._compute_quantity(move.product_uom_qty, self.product_uom, rounding_method='HALF-UP')
        description_picking = self.product_id.with_context(lang=self.request_id.project_id.partner_id.lang or self.env.user.lang)._get_description(self.request_id.picking_type_id)
        template = {
            # truncate to 2000 to avoid triggering index limit error
            # TODO: remove index in master?
            'name': (self.name or '')[:2000],
            'product_id': self.product_id.id,
            'product_uom': self.product_uom_id.id,
            'date': self.request_id.date_approve,
            #'date_expected': self.date_planned,
            'location_id': self.request_id.location_src_id.id,
            'location_dest_id': self.request_id.location_dest_id.id,#
            'picking_id': picking.id,
            #'partner_id': self.request_id.dest_address_id.id,
            #'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
            'state': 'draft',
            'product_line_id': self.id,
            'company_id': self.request_id.company_id.id,
            'price_unit': price_unit,
            'picking_type_id': self.request_id.picking_type_id.id,
            #'group_id': self.request_id.group_id.id,
            'origin': self.request_id.name,
            #'propagate_date': self.propagate_date,
            #'propagate_date_minimum_delta': self.propagate_date_minimum_delta,
            'description_picking': description_picking,
            #'propagate_cancel': self.propagate_cancel,
            'route_ids': self.request_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.request_id.picking_type_id.warehouse_id.route_ids])] or [],
            'warehouse_id': self.request_id.picking_type_id.warehouse_id.id,
        }
        diff_quantity = self.product_uom_qty - qty
        if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom_id.rounding) > 0:
            pr_line_uom = self.product_uom_id
            quant_uom = self.product_id.uom_id
            product_uom_qty, product_uom = pr_line_uom._adjust_uom_quantities(diff_quantity, quant_uom)
            template['product_uom_qty'] = product_uom_qty
            template['product_uom'] = product_uom.id
            res.append(template)
        return res
        
    def _create_stock_moves(self, picking):
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
        
    def _get_stock_move_price_unit(self):
        self.ensure_one()
        line = self[0]
        price_unit = line.product_id.standard_price
        return price_unit