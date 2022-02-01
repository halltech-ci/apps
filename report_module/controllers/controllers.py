# -*- coding: utf-8 -*-
# from odoo import http


# class ReportModule(http.Controller):
#     @http.route('/report_module/report_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_module/report_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_module.listing', {
#             'root': '/report_module/report_module',
#             'objects': http.request.env['report_module.report_module'].search([]),
#         })

#     @http.route('/report_module/report_module/objects/<model("report_module.report_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_module.object', {
#             'object': obj
#         })
