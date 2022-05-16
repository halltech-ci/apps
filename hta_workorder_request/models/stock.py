# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    product_request_id = fields.Many2one('product.request', string="Product Request", related='move_lines.product_line_id.request_id', readonly = True)
    
    def button_validate(self):
        self.product_request_id._action_done()
        return super(StockPicking, self).button_validate()
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    product_line_id = fields.Many2one('product.request.line', string='Product Request Line', ondelete='set null', index = True, readonly = True, check_company = True)
    product_request = fields.Many2one('product.request', check_company = True, ondelete = 'set null', copy = False)
    product_request_task_id = fields.Many2one('project.task', compute='move_task_id', store=True, check_company=True)
    
    @api.depends('product_request')
    def move_task_id(self):
        for move in self:
            if move.product_request:
                move.product_request_task_id = move.product_request.project_task_id
            else:
                move.product_request_task_id = self.env['project.task']
    
    def _prepare_analytic_line_from_task(self):
        product = self.product_id
        company = self.env.company_id
        task = self.product_request.project_task_id
        analytic_account = task.stock_analytic_account_id or task.project_id.analytic_account_id
        
        if not analytic_account:
            return False
        
        res = {
            'name': task.name + product.name,
            "unit_amount" : self.quantity_done,
            'account_id': analytic_account.id,
            'user_id': self._uid,
            "product_uom_id": self.product_uom.id,
            'company_id': analytic_account.company_id.id or company.id,
            'partner_id': task.partner_id.id or task.project_id.partner_id.id or False,
            'stock_task_id': task.id,
        }
        amount_unit = product.with_context(uom=self.product_uom_id).price_compute('standard_price')[product.id]
        amount = amount_unit * self.quantiy_done or 0.0
        result = round(amount, company_id.currency_id.decimal_places) * -1
        vals = {'amount': result}
        analytic_line_fields = self.env['account.analytic.line']._fields
        if 'ref' in analytic_line_fields:
            vals['ref'] = task.name
        if 'product_id' in analytic_line_fields:
            vals['product_id'] = product.id
        if 'employee_id' in analytic_line_fields:
            vals['employee_id'] = (self.env['hr.employee'].search([('user_id', '=', task.user_id)], limit=1)).id
        # tags + distributions
        if task.stock_analytic_tag_ids:
            vals["tag_ids"] = [(6, 0, task.stock_analytic_tag_ids.ids)]
            new_amount = 0
            distributions = self.env["account.analytic.distribution"].search(
                [
                    ("account_id", "=", analytic_account.id),
                    ("tag_id", "in", task.stock_analytic_tag_ids.ids),
                    ("percentage", ">", 0),
                ]
            )
            for distribution in distributions:
                new_amount -= (amount / 100) * distribution.percentage
            vals["amount"] = new_amount
        res.update(vals)
        return res

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    task_id = fields.Many2one('project.task', store=True, compute='_compute_task_id')
    
    @api.depends('move_id')
    def _compute_task_id(self):
        for item in self:
            item.task = item.move_id.task_id or self.env['project.task']