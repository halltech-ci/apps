# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    create_project = fields.Selection(selection=[('add_to_project', "Use project"), ('create_project', "Create Project"),], default='add_to_project')
    project_id = fields.Many2one('project.project', readonly=False)
    state = fields.Selection(selection_add=[('create_project', 'Project'),])
    
    
    def action_create_project(self):
        for rec in self:
            rec.state = 'create_project'
            
    #@api.depends("create_project")
    def create_project_sale_confirm(self):
        """ Generate project for the given so, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        self.ensure_one()
        for rec in self:
            if rec.create_project in ('add_to_project'):
                rec.write({'project_id': rec.project_id.id,
                      'state':'create_project',
                      })
            if rec.create_project == "create_project":
                account = rec.analytic_account_id
                if not account:
                    rec._create_analytic_account(prefix=rec.description or rec.name or None)
                    account = rec.analytic_account_id
                values = {
                    'name': rec.description or rec.name,
                    'analytic_account_id': account.id,
                    'partner_id': rec.partner_id.id,
                    #'sale_line_id': self.id,
                    'sale_order_id': rec.id,
                    'active': True,
                    'company_id': rec.company_id.id,
                }
                if self.description:
                    values['project_description'] = rec.description
                project = self.env['project.project'].create(values)
                rec.write({'project_id': project.id,
                      'state':'create_project',
                      })
            