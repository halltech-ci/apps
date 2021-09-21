# -*- coding: utf-8 -*-
# from odoo import http


# class HtaReport(http.Controller):
#     @http.route('/hta_report/hta_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_report/hta_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_report.listing', {
#             'root': '/hta_report/hta_report',
#             'objects': http.request.env['hta_report.hta_report'].search([]),
#         })

#     @http.route('/hta_report/hta_report/objects/<model("hta_report.hta_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_report.object', {
#             'object': obj
#         })
