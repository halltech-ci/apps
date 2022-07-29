# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date, datetime, timedelta


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'
    
    date_approve = fields.Date(string="Date Approve")
    purchase_status = fields.Selection(selection=[('no', "Non Commandé"), ('partial', "Commandé Partiellement"), ('purchased', "Commandé Totalement"),], compute="_compute_purchase_status", string="Status Commande DA", store=True,)
    stock_status = fields.Selection(selection=[('no', "Non Reçu"), ('partial', "Reçu Partiellement"), ('received', "Reçu Totalement"),], compute="_compute_stock_status", string="Status Reception DA", store=True,)
    
    
    @api.depends('line_ids.purchase_state')
    def _compute_purchase_status(self):
        for req in self:
            pr_status = 'no'
            if req.line_ids:    
                if req.purchase_count > 0:
                    if all([line.purchase_state == 'done' for line in req.line_ids]):
                        pr_status = 'purchased'
                    if any([line.purchase_state == 'purchase' for line in req.line_ids]):
                        pr_status = 'partial'
                else:
                    pr_status = 'no'
            req.purchase_status = pr_status
            
    @api.depends('line_ids.purchased_qty', 'line_ids.product_qty')
    def _compute_stock_status(self):
        for req in self:
            #pr_status = 'no'
            if req.move_count == 0:
                st_status = 'no'
            else:
                st_status = 'received'  
            req.stock_status = st_status
            
    def button_approved(self):
        res = super(PurchaseRequest, self).button_confirm()
        self.write({"date_approve": date.today()})
        return res


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"
    
    
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