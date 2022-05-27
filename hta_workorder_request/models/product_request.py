# -*- coding: utf-8 -*-


from odoo import api, fields, models, _
from odoo.fields import first
from odoo.tools.float_utils import float_compare
from dateutil import relativedelta
from odoo.exceptions import UserError


REQUEST_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To Approve"),
    ("open", "In progress"),
    ("done", "Done"),
    ('close', 'Closed'),
    ("cancel", "Cancelled"),
]

class ProductRequest(models.Model):
    _name ="product.request"
    _description = "Product request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    #Set default picking type to internal
    @api.model
    def _default_picking_type(self):
        company_id = self.env.context.get("company_id") or self.env.user.company_id.id
        return self.env["stock.picking.type"].search([("code", "=", "internal"), ("warehouse_id.company_id", "=", company_id),], limit=1)
    
    @api.model
    def _get_default_picking_type(self):
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        return self.env['stock.picking.type'].search([('code', '=', 'internal'), ('warehouse_id.company_id', '=', company_id), ], limit=1).id
    
    @api.model
    def _get_default_location_src_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self.env.context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_src_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False

    @api.model
    def _get_default_location_dest_id(self):
        location = False
        company_id = self.env.context.get('default_company_id', self.env.company.id)
        if self._context.get('default_picking_type_id'):
            location = self.env['stock.picking.type'].browse(self.env.context['default_picking_type_id']).default_location_dest_id
        if not location:
            location = self.env['stock.warehouse'].search([('company_id', '=', company_id)], limit=1).lot_stock_id
        return location and location.id or False
    
    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)
    
    @api.model
    def _default_warehouse_id(self):
        company = self.env.company.id
        warehouse_ids = self.env['stock.warehouse'].search([('company_id', '=', company)], limit=1)
        return warehouse_ids
    
    name = fields.Char(string="Request Reference", required=True, track_visibility="onchange", default='/', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, index=True, required=True)
    state = fields.Selection(selection=REQUEST_STATES,
        string="Status",
        copy=False,
        default="draft",
        index=True,
        readonly=True,
        track_visibility="onchange",
    )
    date = fields.Datetime(readonly=True, default=fields.Datetime.now, string="Date")
    date_approve = fields.Datetime('Date Approve', readonly=1, index=True, copy=False)
    line_ids = fields.One2many(comodel_name="product.request.line", inverse_name="request_id", string="Products to request", readonly=False, copy=True, track_visibility="onchange",)
    requested_by = fields.Many2one("res.users",
        string="Requested by",
        required=True,
        copy=False,
        track_visibility="onchange",
        default=_get_default_requested_by,
        index=True,
    )
    #Manage analytic
    project_task_id = fields.Many2one('project.task', string="Project Task", domain = "[('project_id', '=', project_id)]")
    project_id = fields.Many2one('project.project', string="Project",)
    analytic_account_id = fields.Many2one("account.analytic.account", related="project_id.analytic_account_id", string="Analytic Account", track_visibility="onchange", )
    #Manage stock for product request
    picking_ids = fields.One2many('stock.picking', 'product_request_id', string='Transfers')
    picking_count = fields.Integer(string='Picking Orders', compute='_compute_picking_ids', default=0)
    #Adding new picking type id
    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type', related="project_id.picking_type", )    
    #Manage stock location.
    location_src_id = fields.Many2one("stock.location", string="Emplacement Source", required=True, related="project_id.location_src_id",)
    #Adding destination location
    location_dest_id = fields.Many2one(string="Destination", comodel_name="stock.location", required=True, related="project_id.location_dest_id")
    #Mange employee timesheet
    timesheet_ids = fields.One2many('account.analytic.line', 'request_id', string="Feuille de temps")
    
    #get default location domain
    def _get_locations_domain(self):
        return ["|", ("company_id", "=", self.env.user.company_id.id), ("company_id", "=", False), ]
        
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
    
    def set_to_draft(self):
        if self.state in ['done', 'close']:
            raise ValidationError(_("Vous ne pouvez pas reinitialiser un OT déja traité"))
        for line in self.line_ids:
            line.set_to_draft()
        self.write({'state': 'draft'})
           
    def button_approve(self):
        #self.is_approver_check()
        #self._create_picking()
        for line in self.line_ids:
            line.action_approve()
        self.write({"state": "open", 'date_approve': fields.Datetime.now()})
        return True
    
    def action_confirm(self):
        if not self.button_approve():
            raise ValidationError(_("You must approve this request before"))
        if len(self.picking_ids) > 0:
            raise ValidationError(_("You can not confirm request that is already confirm"))
        self._create_picking()
        return True
    
    def _action_done(self):
        for line in self.line_ids:
            line.action_done()
        return self.write({"state": 'done'})
    
    def action_close_task(self):
        self._action_close_task()
        self._create_analytic_line_from_timesheet
    
    def _action_close_task(self):
        pickings = self.picking_ids.filtered(lambda l:l.state in ['done'])
        for picking in pickings:
            picking._create_stock_analytic_account()
            
    def _create_analytic_line_from_timesheet(self):
        lines = []
        account = self.analytic_account_id
        for sheet in self.timesheet_ids:
            line = (0, 0, {
                    'name' : sheet.name,
                    'employee_id' : sheet.employee_id.id,
                    'amount' : -sheet.employee_id.timesheet_cost * sheet.unit_amount,
                    'unit_amount' : sheet.unit_amount,
                    'task_id': self.project_task_id,
                    'company_id' : self.company_id.id,
                    }
                )
            lines.append(line)
        account.write({'line_ids': lines})
    
    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            if 'company_id' in  vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('product.request') or '/'
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('product.request') or '/'
        request = super(ProductRequest, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(ProductRequest, self).write(vals)
        return res
    
    def unlink(self):
        for request in self:
            if request.state in ('close', 'done'):
                raise UserError(_('Vous ne pouvez pas supprimer un OT déja traité.'))
        return super(ProductRequest, self).unlink()
    
    def _create_picking(self):
        self.ensure_one()
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
            move_line_value = []
            product_lines = request.mapped('line_ids')
            for line in product_lines:
                #create stock_move (move_lines)
                description_picking = line.product_id.with_context(lang=request.project_id.partner_id.lang or self.env.user.lang)._get_description(request.picking_type_id)
                moves = (0, 0, {
                    'name': line.product_id.display_name,
                    'product_id': line.product_id.id,
                    'description_picking': description_picking,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom_id.id,
                    'location_id': location_id.id,
                    'location_dest_id':location_dest_id.id,
                    'price_unit': line.product_id.standard_price,
                    'product_line_id': line.id,
                    'company_id': self.company_id.id,
                    'origin': origin,
                        }
                    )
                move_value.append(moves)
            picking.write({'move_lines': move_value,})
            picking.action_confirm()
            #request._action_done()
        return True