# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ProductTemplateDefaultCode(models.Model):
    _inherit = "product.template"
    
    @api.constrains('default_code')
    def _compare_default_code(self):
        if len(str(self.default_code))!=15:
            raise ValidationError("Le code de l'article %s n'est pas conforme au code demandé" % (self.name))

            
class ProductProductDefaultCode(models.Model):
    _inherit = "product.product"
    
    @api.constrains('default_code')
    def _compare_default_code(self):
        if len(str(self.default_code))!=15:
            raise ValidationError("Le code de l'article %s n'est pas conforme au code demandé" % (self.name))
