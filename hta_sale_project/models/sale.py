# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    create_project = fields.Boolean(default=True)
    project_id = fields.Many2one('project.project')
    
    
    #@api.depends("create_project")
    def create_project_sale_confirm(self):
        """ Generate project for the given so, and link it.
            :param project: record of project.project in which the task should be created
            :return task: record of the created task
        """
        account = self.analytic_account_id
        if not account:
            self._create_analytic_account(prefix=self.name or None)
            account = self.analytic_account_id
        self.ensure_one()
        values = {
            'name': self.name,
            'analytic_account_id': account.id,
            'partner_id': self.partner_id.id,
            #'sale_line_id': self.id,
            'sale_order_id': self.id,
            'active': True,
            'company_id': self.company_id.id,
        }
        # create the project
        values['project_description'] = self.description
        project = self.env['project.project'].create(values)
        self.write({'project_id': project.id})
        #return project
    
    