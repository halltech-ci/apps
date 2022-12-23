# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta

class PurchaseRequest(models.Model):
    _inherit = "purchase.request"
    
    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.request.sequence")
    
    @api.depends('requested_by')
    def _compute_has_manager(self):
        for rec in self:
            if rec.requested_by:
                employee = self.env['hr.employee'].search([('work_email', '=', rec.requested_by.email)], limit = 1)
                if (employee.department_id) and (employee.department_id.manager_id):
                    rec.has_manager = True
                else:
                    rec.has_manager = False
    
    @api.model
    def _default_picking_type(self):
        type_obj = self.env["stock.picking.type"]
        company_id = self.env.context.get("company_id") or self.env.company.id
        types = type_obj.search(
            [("code", "=", "incoming"), ("warehouse_id.company_id", "=", company_id)]
        )
        if not types:
            types = type_obj.search(
                [("code", "=", "incoming"), ("warehouse_id", "=", False)]
            )
        return types[:1]
    
    @api.model
    def _default_date_required(self):
        req_date = date.today() + timedelta(days=7)
        return req_date
               
    name = fields.Char(string="Request Reference", required=True, default='/', index=True, readonly=True)
    request_date = fields.Datetime(string="Request date", help="Date when the user initiated the request.", default=fields.Datetime.now, track_visibility="onchange", readonly=True)
    sale_order = fields.Many2one('sale.order', string='Sale Order')
    project = fields.Many2one('project.project', related="sale_order.project_id", string="Project", readonly=True, store=True)
    project_code = fields.Char(related='project.code', string="Project Code", readonly=True)
    purchase_type = fields.Selection(selection=[('project', 'Matières/Consommables'), ('travaux', 'Travaux'), ('transport', 'Transport'), ('subcontract', 'Sous Traitance'), ('stock', 'Appro'),], string="Type Achat")
    is_project_approver = fields.Boolean(compute='_compute_is_project_approver')
    is_expense = fields.Boolean('is_expense', default=False)
    picking_type_id = fields.Many2one(required=False)
    is_for_project = fields.Boolean(string="Imputer au projet", default=True)
    requested_by = fields.Many2one('res.users', string="Demandeur DA", readonly=True)
    date_required = fields.Date(string="Request Date", track_visibility="onchange", default=lambda self:self._default_date_required())
    date_approve = fields.Date(string="Date Approve")
    
    
    def _compute_is_project_approver(self):
        for req in self:
            user = self.env.user
            if user.has_group('project.group_project_manager'):
                req.is_project_approver = True
            else:
                req.is_project_approver = False
    
    @api.model
    def create(self, vals):
        #request = super(PurchaseRequest, self).create(vals)
        if vals.get('name', '/') == '/':
            seq_date = None
            if 'request_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['request_date']))
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('purchase.request.sequence', sequence_date=seq_date) or '/'
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request.sequence', sequence_date=seq_date) or '/'
        request = super(PurchaseRequest, self).create(vals)
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
        return self.write({"state": "approved", "date_approve": date.today()})
    
    def write(self, vals):
        res = super(PurchaseRequest, self).write(vals)
        return res
    
    
    def unlink(self):
        for request in self:
            if request.line_ids:
                raise UserError(
                    _("Vous ne pouvez plus supprimer de DA. Veuillez la modifier")
                )
        return super(PurchaseRequest, self).unlink()
    
class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"
    
    @api.model
    def get_product_domain(self):
        domain = [("purchase_ok", "=", True)]
        if self.request_id.purchase_type == 'project':
            domain.append(('type', '=', 'product'))
        elif self.request_id.purchase_type != 'project' and self.request_id.purchase_type != False:
            domain.append(('type', 'not in', ('product')))
        return domain
    
    project = fields.Many2one('project.project', string="Project", readonly=True, related="request_id.project")
    product_code = fields.Char(related="product_id.default_code", sting="Code Article", store=True)
    product_tmpl_id = fields.Many2one("product.template", related="product_id.product_tmpl_id")
    #product_attribute_ids = fields.Many2many('product.attribute.', related="product_tmpl_id.product_attribute_ids")
    attribute_line_ids = fields.One2many("product.template.attribute.line", related="product_tmpl_id.attribute_line_ids")
    specifications = fields.Text(default="")
    product_id = fields.Many2one(comodel_name="product.product", string="Product", domain= lambda self:self.get_product_domain(), track_visibility="onchange",)
    purchase_type = fields.Selection(selection=[('project', 'Matières/Consommables'), ('travaux', 'Travaux'), ('transport', 'Transport'), ('subcontract', 'Sous Traitance'), ('stock', 'Appro'),], related='request_id.purchase_type')
    date_required = fields.Date(string="Request Date", required=True, track_visibility="onchange", related="request_id.date_required")
    ordered_qty = fields.Float(compute='_compute_qty_ordered', help="Effective qty buy")
    ordered_price_total = fields.Float(compute='_compute_qty_ordered')
    project_id = fields.Many2one('project.project', compute="_compute_project_id", store=True,)
    
    
    @api.depends('project')
    def _compute_project_id(self):
        for rec in self:
            if rec.project:
                rec.project_id = rec.project
            else:
                rec.project_id = False
        
    
    def _compute_qty_ordered(self):
        for rec in self:
            rec.ordered_qty = 0.0
            rec.ordered_price_total = 0
            for line in rec.purchase_lines.filtered(lambda x: x.state in ["done", "purchase"]):
                if rec.product_uom_id and line.product_uom != rec.product_uom_id:
                    rec.ordered_qty += line.product_uom._compute_quantity(
                        line.product_qty, rec.product_uom_id
                    )
                    rec.ordered_price_total += line.price_subtotal
                else:
                    rec.ordered_qty += line.product_qty
                    rec.ordered_price_total += line.price_subtotal
            
            
    
    @api.depends('request_id.project')
    def compute_project_id(self):
        for line in self:
            if line.request_id.project:
                line.project_id = line.request_id.project
    
    @api.onchange("product_id")
    def onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                name = rec.product_id.name
                if rec.product_id.code:
                    name = "{} ".format(rec.product_id.product_tmpl_id.name)
                    for no_variant_attribute_value in rec.product_id.product_template_attribute_value_ids:
                        name += "{}".format(no_variant_attribute_value.name + ', ')
                if rec.product_id.description_purchase:
                    name += "\n" + rec.product_id.description_purchase
                rec.product_uom_id = rec.product_id.uom_id.id
                rec.product_qty = 1
                rec.name = name
    
    @api.constrains('product_id', 'product_uom_id')
    def _compare_product_uom(self):
        #for line
        if self.product_id:
            if self.product_id.uom_id.category_id != self.product_uom_id.category_id:
                raise ValidationError("Les unite de mesure de %s ne sont pas dans la meme categorie" % (self.product_id.name))
    
    
    @api.onchange('product_uom_id')
    def _onchange_product_uom(self):
        if self.product_id:
            if self.product_id.uom_id.category_id != self.product_uom_id.category_id:
                raise ValidationError("Les unite de mesure de %s ne sont pas dans la meme categorie" % (self.product_id.name))