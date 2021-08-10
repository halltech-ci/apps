# -*- coding: utf-8 -*-
# from odoo import http


# class HtaDocumentSign(http.Controller):
#     @http.route('/hta_document_sign/hta_document_sign/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_document_sign/hta_document_sign/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_document_sign.listing', {
#             'root': '/hta_document_sign/hta_document_sign',
#             'objects': http.request.env['hta_document_sign.hta_document_sign'].search([]),
#         })

#     @http.route('/hta_document_sign/hta_document_sign/objects/<model("hta_document_sign.hta_document_sign"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_document_sign.object', {
#             'object': obj
#         })
