# -*- coding: utf-8 -*-
# from odoo import http


# class HtaSaleSequence(http.Controller):
#     @http.route('/hta_sale_sequence/hta_sale_sequence/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_sale_sequence/hta_sale_sequence/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_sale_sequence.listing', {
#             'root': '/hta_sale_sequence/hta_sale_sequence',
#             'objects': http.request.env['hta_sale_sequence.hta_sale_sequence'].search([]),
#         })

#     @http.route('/hta_sale_sequence/hta_sale_sequence/objects/<model("hta_sale_sequence.hta_sale_sequence"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_sale_sequence.object', {
#             'object': obj
#         })
