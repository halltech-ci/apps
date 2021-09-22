# -*- coding: utf-8 -*-
# from odoo import http


# class HtaDocumentCustom(http.Controller):
#     @http.route('/hta_document_custom/hta_document_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_document_custom/hta_document_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_document_custom.listing', {
#             'root': '/hta_document_custom/hta_document_custom',
#             'objects': http.request.env['hta_document_custom.hta_document_custom'].search([]),
#         })

#     @http.route('/hta_document_custom/hta_document_custom/objects/<model("hta_document_custom.hta_document_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_document_custom.object', {
#             'object': obj
#         })
