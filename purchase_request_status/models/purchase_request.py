# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'
    
    purchase_status = fields.Selection(selection=[('no', "Non Commandé"), ('partial', "Commandé Partiellement"), ('purchased', "Commandé Totalement"),], compute="_compute_purchase_status", string="Status Commande DA", store=True,)
    stock_status = fields.Selection(selection=[('no', "Non Reçu"), ('partial', "Reçu Partiellement"), ('received', "Reçu Totalement"),], compute="_compute_stock_status", string="Status Reception DA", store=True,)
    #purchase_order_count = fields.Integer(string="Purchases count", compute="_compute_po_count", readonly=True)
    
    @api.depends('line_ids.purchase_state')
    def _compute_purchase_status(self):
        for order in self:
            pr_status = 'no'
            state = []
            if all([line.purchase_state in ('purchase', 'done') for line in order.line_ids]):
                pr_status = 'purchased'
            elif any([line.purchase_state in ('purchase','done') for line in  order.line_ids]):
                pr_status = 'partial'
            order.purchase_status = pr_status
            
    @api.depends('line_ids.stock_state')
    def _compute_stock_status(self):
        for req in self:
            st_status = 'no'
            if req.move_count > 0:
                if all([line.stock_state == "done" for line in req.line_ids]):
                    st_status = 'received'
                elif any([line.stock_state == "partially_available" for line in req.line_ids]):
                    st_status = 'partial'
            else:
                st_status = 'no'  
            req.stock_status = st_status

class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"
    
    
    stock_state = fields.Selection(compute="_compute_stock_state", string="Stock Status", selection=lambda self: self.env["stock.move"]._fields["state"].selection, store=True,)
    
    @api.depends("purchase_lines.state", "purchase_lines.order_id.state")
    def _compute_purchase_state(self):
        for rec in self:
            temp_purchase_state = False
            if rec.purchase_lines:
                if all([po_line.state == "done" for po_line in rec.purchase_lines]):
                    temp_purchase_state = "done"
                elif all([po_line.state == "cancel" for po_line in rec.purchase_lines]):
                    temp_purchase_state = "cancel"
                elif any(
                    [po_line.state == "purchase" for po_line in rec.purchase_lines]
                ):
                    temp_purchase_state = "purchase"
                elif any(
                    [po_line.state == "to approve" for po_line in rec.purchase_lines]
                ):
                    temp_purchase_state = "to approve"
                elif any([po_line.state == "sent" for po_line in rec.purchase_lines]):
                    temp_purchase_state = "sent"
                elif all(
                    [
                        po_line.state in ("draft", "cancel")
                        for po_line in rec.purchase_lines
                    ]
                ):
                    temp_purchase_state = "draft"
            rec.purchase_state = temp_purchase_state
            
            
    @api.depends("purchase_request_allocation_ids.stock_move_id.state")
    def _compute_stock_state(self):
        for rec in self:
            st_state = False
            if rec.purchase_request_allocation_ids.stock_move_id:
                if all([line.state == "done" for line in rec.purchase_request_allocation_ids.stock_move_id]):
                    st_state = "done"
                elif any([line.state == 'done' for line in rec.purchase_request_allocation_ids.stock_move_id]):
                    st_state = "partially_available"
            rec.stock_state = st_state
