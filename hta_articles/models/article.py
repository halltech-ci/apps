import re
from collections import defaultdict
from string import Template
from odoo import _, api, fields, models



class ProductTemplate(models.Model):
    _inherit = "product.template"

    code_prefix = fields.Char(help="Add prefix to product variant reference (default code)",)
    
    code_mesure = fields.Char()
    
    
    
    @api.onchange("categ_id")
    def _compute_code_prefix(self):
        for rec in self:
            if rec.categ_id:
                rec.name = rec.categ_id.l_name