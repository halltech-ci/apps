# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.project"
    
    code = fields.Char(string="Project Number", required=True, default="/", readonly=True)

    _sql_constraints = [
        ("project_unique_code", "UNIQUE (code)", _("The code must be unique!"))
    ]
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "/") == "/":
                vals["code"] = self.env["ir.sequence"].next_by_code("project.code")
        return super().create(vals_list)
    
    
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default["code"] = self.env["ir.sequence"].next_by_code("project.code")
        return super().copy(default)

    def name_get(self):
        result = super().name_get()
        new_result = []

        for project in result:
            rec = self.browse(project[0])
            name = "[{}] {}".format(rec.code, project[1])
            new_result.append((rec.id, name))
        return new_result
