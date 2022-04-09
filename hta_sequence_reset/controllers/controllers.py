# -*- coding: utf-8 -*-
# from odoo import http


# class HtaSequenceReset(http.Controller):
#     @http.route('/hta_sequence_reset/hta_sequence_reset/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_sequence_reset/hta_sequence_reset/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_sequence_reset.listing', {
#             'root': '/hta_sequence_reset/hta_sequence_reset',
#             'objects': http.request.env['hta_sequence_reset.hta_sequence_reset'].search([]),
#         })

#     @http.route('/hta_sequence_reset/hta_sequence_reset/objects/<model("hta_sequence_reset.hta_sequence_reset"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_sequence_reset.object', {
#             'object': obj
#         })
