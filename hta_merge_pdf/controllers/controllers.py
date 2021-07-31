# -*- coding: utf-8 -*-
# from odoo import http


# class HtaMergePdf(http.Controller):
#     @http.route('/hta_merge_pdf/hta_merge_pdf/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_merge_pdf/hta_merge_pdf/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_merge_pdf.listing', {
#             'root': '/hta_merge_pdf/hta_merge_pdf',
#             'objects': http.request.env['hta_merge_pdf.hta_merge_pdf'].search([]),
#         })

#     @http.route('/hta_merge_pdf/hta_merge_pdf/objects/<model("hta_merge_pdf.hta_merge_pdf"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_merge_pdf.object', {
#             'object': obj
#         })
