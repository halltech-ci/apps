from odoo import models, fields, api

class AttributLine(models.Model):
    _name = 'codification.attribute'
    _description = 'Codification attribute'
    
    name = fields.Char("Attribute Name")
    #valus = fields.Char(String="Valeurs")
    #attribute_value = fields.One2many('attribute.attribute','attribut_id')
    #attribute_ids = fields.One2many('codification.attribute', 'request_id')
    #value_ids = fields.Many2many('attribute.attribute','Values')
    attribute_id = fields.Many2one('attribute.attribute','Attribute')
    
    
    
class AttributeAttribute(models.Model):
    _name = 'attribute.attribute'
    _description = 'Attribute attribute'
    
    name = fields.Char("Attribute Name")
    valus = fields.Char("Valeurs")
    request_id = fields.Many2one('code.request')
    
   