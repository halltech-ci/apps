# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    create_project = fields.Selection(selection=[('add_to_project', "Use project"), ('create_project', "Create Project"),], default='add_to_project')
    project_id = fields.Many2one('project.project', readonly=False, copy=False)
    project_template = fields.Many2one('project.project', string='Modele projet', domain="[('is_template', '=', True)]")
    state = fields.Selection(selection_add=[('done', 'Projet')])
    project_description = fields.Text(string="Decription du Projet")
    has_project = fields.Boolean(compute = '_compute_has_project_id',)
    analytic_group = fields.Many2one('account.analytic.group', string='Groupe Analytic')
    #state = fields.Selection(selection_add=[('done', 'Projet')])
    
    #@api.depends('project_id')
    def _compute_has_project_id(self):
        for rec in self:
            rec.has_project = False
            if rec.project_id:
                rec.has_project = True
    
    def action_create_project(self):
        for rec in self:
            rec.state = 'done'                
    
    #@api.depends("create_project")
    def create_project_sale_confirm(self):
        """ Generate project for the given so, and link it.
            :param project or project template: record of project.project in which the task should be created
            :return task: record of the created task
        """
        self.ensure_one()
        for rec in self:
            if rec.create_project in ('add_to_project'):
                project = rec.project_id
            if rec.create_project == "create_project":
                account = rec.analytic_account_id
                if not account:
                    rec._create_analytic_account(prefix=rec.description or rec.name or None)
                    account = rec.analytic_account_id
                account.write({'group_id': rec.analytic_group})
                values = {
                    'name': rec.project_description or rec.name,
                    'analytic_account_id': account.id,
                    'partner_id': rec.partner_id.id,
                    'sale_order_id': rec.id,
                    'active': True,
                    'company_id': rec.company_id.id,
                }
                project = self.env['project.project'].create(values)
            rec.write({'project_id': project.id, 'state':'done',})
        return project
            