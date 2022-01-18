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
    #request_code_id = fields.Many2one('product.attribute', string="Stock", tracking=True, states=READONLY_STATES)
    #is_code_product = fields.Boolean(string="Is Validate",compute="_compute_is_code_product",)
    #==============================================

    
    type_product = fields.Selection([
        ('consu', 'Consommable'),
        ('service', 'Service'), 
        ('product', 'Produit stockable'),     
    ], default='consu', String="Type produit")
    
    date = fields.Datetime("Date demande",readonly=True, default=fields.Datetime.now)
    caracteristique = fields.One2many('attribute.attribute','request_id', copy=True)
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
            
            product_template.create({"name":name,
                                   "type":type_product,
                                   })    
        return True
    
    def create_product_category(self):
        for request in self:
            product_category = self.env["product.category"]
            family = request.family
            sous_family = request.sous_family
            
            cat_family = product_category.create({
                                    "name":family,
                                    #"parent_id":family,
                                   })
            if cat_family:
                product_category.create({
                                    "name":sous_family,
                                    "parent_id":cat_family.id,
                                   })   
        return True
            
    def create_product_attribute(self):
        for rec in self:
            product_attribute = self.env["product.attribute"]
            value_lines = rec.mapped('caracteristique')
            value = []
            for line in value_lines:
                product_attribute.create({"name":line.attribute_name,"value_ids":line.attribute_valus,})
            
                #product_attribute.create({"name": line.attribute_name,
                                          #"value_ids": line.attribute_valus,})
            
        #return True
    
    
    def button_validate(self):
        category = self.create_product_category()
        template = self.create_product_template()
        attribute = self.create_product_attribute()
        validate = (template,attribute,category)
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