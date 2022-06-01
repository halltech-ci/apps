# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    
    has_project = fields.Boolean(compute = '_compute_has_project_id',)
    project_template = fields.Many2one('project.project', string='Modele projet', domain="[('is_template', '=', True)]")
    project_description = fields.Text(string="Decription du Projet")
    
    def _compute_has_project_id(self):
        for rec in self:
            rec.has_project = False
            if rec.project_id:
                rec.has_project = True
    
    def _action_confirm(self):
        result = super(SaleOrder, self)._action_confirm()
        for order in self:
            if not order.has_project and order.description == '':
                raise ValidationError(_('Vous devez indiquer une description du projet.'))
            order.create_project_from_sale()
        return result
    
    def _generate_project_value(self):
        account = self.analytic_account_id
        if not account:
            self._create_analytic_account(prefix=self.description or self.name or None)
            account = self.analytic_account_id
        return {
            'name': self.client_order_ref if self.client_order_ref else self.description or self.name,
            'analytic_account_id': account.id,
            'partner_id': self.partner_id.id,
            #'sale_line_id': self.id,
            'sale_order_id': self.id,
            'active': True,
            'company_id': self.company_id.id,
        }
    
    def create_project_from_sale(self):
        values = self._generate_project_value()
        project = self.env['project.project']
        if self.has_project:
            pass
        if self.project_template:
            project = self.project_template.copy(values)
            self.write({'project_id': project.id})
        else:
            project.create(values)
            self.write({'project_id': project.id})
        return project
    
            
        