from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

READONLY_STATES = {
        'to_cancel': [('readonly', True)],
        }


class CodificationRequest(models.Model):
    _name = 'code.request'
    _description = 'Codification request'
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'
    
    
    object = fields.Char('Objet', tracking=True)
    family = fields.Char('Famille',required=True, tracking=True)
    sous_family = fields.Char('Sous Famille',required=True, tracking=True)
    name = fields.Char('Product Name',required=True, tracking=True)
    #================ajoute=======================
    request_code_id = fields.Many2one('product.attribute', string="Stock", tracking=True, states=READONLY_STATES)
    #is_code_product = fields.Boolean(string="Is Validate",compute="_compute_is_code_product",)
    #==============================================

    
    type_product = fields.Selection([
        #('storable', 'Produit stockable'),
        ('service', 'Service'),
        ('consu', 'Consumable'),      
    ], default='Consumable', String="Type produit")
    
    date = fields.Datetime("Date demande",readonly=True, default=fields.Datetime.now)
    caracteristique = fields.One2many('attribute.attribute','request_id')
    description = fields.Text("Description")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('validate', 'Validate'),
        ('cancel', 'Annuler'),
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', help='Codification Report State')
        
    def button_submit(self):
        for line in self.caracteristique:
            line.action_submit()
        self.state = "submit"
        return True

    #def button_fait(self):
        #self.state = "fait"
        
    def button_cancel(self):
        return self.write({'state': 'to_cancel'})
    
    def create_product_template(self):
        for request in self:
            product_template = self.env["product.template"]
            family = request.family
            sous_family = request.sous_family
            name = request.name
            type_product = request.type_product
            
            product_template.create({"name":str(request.name),
                                   "type":str(request.type_product),
                                    "categ_id":str(request.family),
                                   #"categ_id":request.sous_family,
                                   })    
        return True
            
    def create_product_attribute(self):
        for rec in self:
            attribute_name = rec.caracteristique.attribute_name
            attribut_valus = rec.caracteristique.attribute_valus
            
            product_attribute = self.env["product.attribute"]
            product_attribute.write({"name":attribute_name,
                                     "display_type":'select'})
            product_attribute.write({"value_ids":attribute_valus})
            
            value_lines = rec.mapped('caracteristique')
            value = []
            for line in value_lines:
                project_id = line.project.id
                lines = (0, 0, {
                    "value_ids": line.attribute_valus.id,
                })
                value.append(lines)
            request_code_id.write({'caracteristique': value})
        return True
    
    
    def button_validate(self):
        template = self.create_product_template()
        #attribute = self.create_product_attribute()
        validate = template
        if validate:
            for line in self.caracteristique:
                line.action_validate()
            return self.write({'state': 'validate'})
        #return True
    
    
    #@api.model
    #def create(self, vals):
        #request = super(CodificationRequest, self).create(vals)
        #return request
    
    #def write(self, vals):
        #res = super(CodificationRequest, self).write(vals)
        #return res
    
    #def unlink(self):
        #if any(self.filtered(lambda code: code.state not in ('draft', 'submitted', 'cancel'))):
            #raise UserError(_('You cannot delete an expense which is not draft, cancelled or submitted!'))        
        #return super(CodificationRequest, self).unlink()
        
        
    #===================================
    #def is_approver_check(self):
        #for rec in self:
            #if not rec.is_code_product:
                #raise UserError(
                    #_(
                        #"You are not allowed to approve this expense request "
                        #". (%s)"
                    #)
                    #% rec.name
                #)
        
        