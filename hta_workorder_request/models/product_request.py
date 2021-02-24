# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

REQUEST_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To Approve"),
    ("open", "In progress"),
    ("done", "Done"),
    ("cancel", "Cancelled"),
]

class ProductRequest(models.Model):
    _name ="product.request"
    _description = "Product request"
    
    @api.model
    def _default_picking_type(self):
        return self._get_picking_type(self.env.context.get('company_id') or self.env.company.id)
    
    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)
    
    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("product.request")
    
    @api.model
    def _default_warehouse_id(self):
        company = self.env.company.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids
    
    name = fields.Char(string="Request Reference", required=True,
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
    date_approve = fields.Datetime('Date Approve', readonly=1, index=True, copy=False)
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
    #Manage analytic
    project_task_id = fields.Many2one('project.task', string="Project Task")
    project_id = fields.Many2one('project.project', string="Project")
    analytic_account_id = fields.Many2one("account.analytic.account",
        string="Analytic Account",
        track_visibility="onchange",
    )
    #Manage stock for product request
    #picking_id = fields.Many2one('stock.picking')
    picking_ids = fields.One2many('stock.picking', 'product_request_id', string='Transfers')
    picking_count = fields.Integer(string='Picking Orders', compute='_compute_picking_ids', default=0)
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type',
        default=_default_picking_type,
    )
    picking_policy = fields.Selection([('direct', 'As soon as possible'),
        ('one', 'When all products are ready')],
        string='Picking Policy', required=True, readonly=True, default='direct',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}
        ,help="If you deliver all products at once, the delivery order will be scheduled based on the greatest "
        "product lead time. Otherwise, it will be based on the shortest.")
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
        required=True, readonly=True, 
        states={'draft': [('readonly', False)], 'to_approve': [('readonly', False)]},
        default=_default_warehouse_id, check_company=True
    )
    location_src_id = fields.Many2one('stock.location', 'Source Location', related='picking_type_id.default_location_src_id')
    location_dest_id = fields.Many2one('stock.location', 'Dest Location',)
    
    @api.model
    def _get_picking_type(self, company_id):
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('warehouse_id.company_id', '=', company_id)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing'), ('warehouse_id', '=', False)])
        return picking_type[:1]
    
    @api.depends('picking_ids')
    def _compute_picking_ids(self):
        for request in self:
            request.picking_count = len(request.picking_ids)
    
    def action_view_picking(self):
        '''
        This function returns an action that display existing delivery orders
        of given product request ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('stock.action_picking_tree_all').read()[0]

        pickings = self.mapped('picking_ids')
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    
    @api.onchange('project_task_id')
    def _onchange_project_task_id(self):
        for rec in self:
            data = self.env['project.task'].search([('id', '=', rec.project_task_id.id)]).mapped('product_lines')
            lines = [(5, 0, 0)]
            for line in data:
                lines.append((4, line.id, 0))
            rec.line_ids = lines
    
    def button_to_approve(self):
        #self.to_approve_allowed_check()
        #self.is_approver_check()
        for line in self.line_ids:
            line.action_to_approve()
        return self.write({"state": "to_approve"})
    
    def button_approve(self):
        #self.is_approver_check()
        self._create_picking()
        for line in self.line_ids:
            line.action_approve()
        return self.write({"state": "open", 'date_approve': fields.Datetime.now()})
    
    def _action_done(self):
        for line in self.line_ids:
            line.action_done()
        return self.write({"state": 'done'})
        
    
    @api.model
    def create(self, vals):
        request = super(ProductRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(ProductRequest, self).write(vals)
        return res
    
    def _create_picking(self):
        for request in self:
            #prepare picking
            picking_type_id = request.picking_type_id
            location_id = request.location_src_id
            location_dest_id = request.location_dest_id
            origin = request.name
            company_id = request.company_id
            date = request.date_approve
            picking_value = {
                'picking_type_id': picking_type_id.id,
                'location_id': location_id.id,
                'origin': origin,
                'company_id': self.company_id.id,
                'date': date,
                'location_id':picking_type_id.default_location_src_id.id,
                'location_dest_id': location_dest_id.id
            }
            picking = self.env['stock.picking'].create(picking_value)
            move_value = []
            product_lines = request.mapped('line_ids')
            for line in product_lines:
                #create stock_move (move_lines)
                description_picking = line.product_id._get_description(request.picking_type_id)
                moves = (0, 0, {
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'description_picking': description_picking,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom_id.id,
                    'location_id': location_id.id,
                    'location_dest_id':location_dest_id.id,
                    'price_unit': line.product_id.standard_price,
                    'product_line_id': line.id,
                    'company_id': self.company_id.id,
                        }
                    )
                move_value.append(moves)
            picking.write({'move_lines': move_value})
        return True
                
            
    

    
    