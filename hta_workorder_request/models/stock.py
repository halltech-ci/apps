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
            moves = picking.mapped('move_lines').filtered(lambda move:move.state == 'done')
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
                    'product_line': move.product_line_id,
                    }
                )
                if qty_done > 0 :
                    lines.append(move_line)
            analytic_account.sudo().write({'line_ids' : lines})
        return True
    
    def _create_delivery_picking(self):
        self.ensure_one()
        for picking in self:
            moves = []
            picking_type = self.env['stock.picking.type'].search([('company_id', '=', picking.company_id.id), ('code', '=', 'outgoing')], limit=1)
            location_id = self.env['stock.location'].search([('barcode', '=', 'WH-OUTPUT')])
            origin = picking.origin
            picking_value = {
                'picking_type_id': picking_type.id,
                'location_id': location_id.id,
                'location_dest_id' : picking_type.default_location_dest_id.id,
                'origin' : origin,
                'company_id' : picking.company_id.id,
            }
            delivery_picking = self.env['stock.picking'].create(picking_value)
            move_value = []
            for move in picking.mapped('move_line_ids'):
                description_picking = move.product_id.with_context(lang=move.move_id.product_line_id.project_id.partner_id.lang or self.env.user.lang)._get_description(picking_type)
                moves = (0, 0, {
                        'name': move.product_id.display_name,
                        'product_id': move.product_id.id,
                        'description_picking': description_picking,
                        'product_uom_qty': move.qty_done,
                        'product_uom': move.product_uom_id.id,
                        'location_id': location_id.id,
                        'location_dest_id': picking_type.default_location_dest_id.id,
                        'price_unit': move.product_id.standard_price,
                        #'product_line_id': move.product_line_id.id,
                        'company_id': picking.company_id.id,
                        'origin': origin,
                            }
                        )
                move_value.append(moves)
            delivery_picking.write({'move_lines': move_value,})
            delivery_picking.action_confirm()
            
    
    #def _create_delivery_picking(self):
        
    
    def button_validate(self):
        self.product_request_id._action_done()
        return super(Picking, self).button_validate()
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_line_id = fields.Many2one('product.request.line', string='Product Request Line')
    #analytic_line = fields.Many2one('account.analytic.line', string="Analytic line", compute = '_compute_analytic_line')
    
    def _action_assign(self):
        return super(StockMove, self)._action_assign()
    
    @api.depends('product_line_id.analytic_line')
    def _compute_analytic_line(self):
        for move in self:
            move.analytic_line = move.product_line_id.analytic_line
            
"""class StockMoveLine(self):
    _inherit = 'stock.move.line'
    
    product_line_id = fields.Many2one('product.request.line', related="move_id.product_line_id",string='Product Request Line')
"""  
    
            
            
            