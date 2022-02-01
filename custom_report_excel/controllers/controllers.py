# -*- coding: utf-8 -*-
# from odoo import http


# class CustomReportExcel(http.Controller):
#     @http.route('/custom_report_excel/custom_report_excel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_report_excel/custom_report_excel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_report_excel.listing', {
#             'root': '/custom_report_excel/custom_report_excel',
#             'objects': http.request.env['custom_report_excel.custom_report_excel'].search([]),
#         })

#     @http.route('/custom_report_excel/custom_report_excel/objects/<model("custom_report_excel.custom_report_excel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_report_excel.object', {
#             'object': obj
#         })
