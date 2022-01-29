# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCodificationRequest(http.Controller):
#     @http.route('/hta_codification_request/hta_codification_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_codification_request/hta_codification_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_codification_request.listing', {
#             'root': '/hta_codification_request/hta_codification_request',
#             'objects': http.request.env['hta_codification_request.hta_codification_request'].search([]),
#         })

#     @http.route('/hta_codification_request/hta_codification_request/objects/<model("hta_codification_request.hta_codification_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_codification_request.object', {
#             'object': obj
#         })
