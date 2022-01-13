from odoo import models, fields, api, _
#from odoo.exceptions import UserError, ValidationError


class CodificationRequest(models.Model):
    _name = 'code.request'
    _description = 'Codification request'
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'
    
    
    
    family = fields.Char('Famille',required=True,)
    sous_family = fields.Char('Sous Famille',required=True,)
    name = fields.Char('Product Name',required=True,)
    type_product = fields.Selection([
        ('storable', 'Produit stockable'),
        ('service', 'Service'),
        ('consumable', 'Consommable'),
    ], default='storable', String="Type produit")
    date = fields.Date("Date demande")
    attribute_ids = fields.One2many('attribute.attribute','request_id',String='Attribute Values')
    description = fields.Text(String="Description")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('approuve', 'Approuve'),
        ('validate', 'Validate'),
        ('fait', 'Fait'),
        ('annuler', 'Annuler'),
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Codification Report State')
    
    def action_approuve(self):
        self.state = "approuve"
        
    def to_validate(self):
        self.state = "validate"
        
    def button_fait(self):
        self.state = "fait"
        
    def button_cancel(self):
        self.state = "cancel"
    
    

    
    
    
    
   
    