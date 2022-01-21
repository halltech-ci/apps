from odoo import models, fields, api

REQUEST_STATE = [('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('validate', 'Validate'),
        ('cancel', 'Annuler')
        ]


class AttributeAttribute(models.Model):
    _name = 'attribute.attribute'
    _description = 'Attribute attribute'
    
    attribute_name = fields.Char("Attribute Name")
    attribute_valus = fields.Many2many('codification.attribute')
    request_id = fields.Many2one('code.request')
    
    #======================ajoute===========
    request_state = fields.Selection(selection=REQUEST_STATE, string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True, help='Expense Report State')
    
    def action_submit(self):
        for rec in self:
            self._action_submit()

    def _action_submit(self):
        for rec in self:
            self.request_state = "submit"
    
    def action_validate(self):
        for rec in self:
            self.request_state = "validate"
        
    def do_cancel(self):
        for rec in self:
            """Actions to perform when cancelling a expense line."""
            self.write({"request_state": 'draft'})

            
            
            


class AttributLine(models.Model):
    _name = 'codification.attribute'
    _description = 'Codification attribute'
    
    name = fields.Char("Attribute Name")
    attribute_id = fields.Many2one('attribute.attribute','Attribute')
        
