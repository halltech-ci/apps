# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Picking(models.Model):
    _inherit = "stock.picking"
    
    product_request_id = fields.Many2one('product.request', string="Product Request", related='move_lines.product_line_id.request_id',)
    #account_analytic_id = fields.Many2one()
    
    def _create_stock_analytic_account(self):
        self.ensure_one()
        
        for picking in self:
            if picking.state not in ['done'] :
                continue
            moves = picking.mapped('move_lines')
            analytic_account = picking.product_request_id.analytic_account_id
            #analytic_line = self.env['account.analyitc.line'].sudo()
            lines = []
            for move in moves:
                qty_done = move.quantity_done
                move_line = (0, 0, {
                    'name' : move.name,
                    'amount' : -move.price_unit * move.quantity_done,
                    #'account_id' : analytic_account.id,
                    'ref' : move.reference,
                    'unit_amount' : move.quantity_done,
                    'move_id' : move.id,
                    'company_id' : move.company_id.id,
                    'product_id' : move.product_id.id,
                    }
                )
                if qty_done > 0 :
                    lines.append(move_line)
            analytic_account.sudo().write({'line_ids' : lines})
        return True
    
    def button_validate(self):
        self.product_request_id._action_done()
        return super(Picking, self).button_validate()
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_line_id = fields.Many2one('product.request.line', string='Product Request Line')
    
    def _action_assign(self):
        return super(StockMove, self)._action_assign()
            
            
        