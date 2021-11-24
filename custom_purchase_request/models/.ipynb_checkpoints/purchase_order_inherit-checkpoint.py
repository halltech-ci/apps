# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words
from odoo.addons import decimal_precision as dp

class custom_purchase_request(models.Model):
    _inherit = "purchase.order"
    
    #num2words convert number to word
    def _num_to_words(self, num):
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()
        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

    amount_to_word = fields.Char(string="Amount In Words:", compute='_compute_amount_to_word')
    
    def _compute_amount_to_word(self):
        for rec in self:
            rec.amount_to_word = str(self._num_to_words(rec.amount_total)).upper()