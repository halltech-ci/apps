# -*- coding: utf-8 -*-
# from odoo import http


# class HtaSaleExcelReport(http.Controller):
#     @http.route('/hta_sale_excel_report/hta_sale_excel_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_sale_excel_report/hta_sale_excel_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_sale_excel_report.listing', {
#             'root': '/hta_sale_excel_report/hta_sale_excel_report',
#             'objects': http.request.env['hta_sale_excel_report.hta_sale_excel_report'].search([]),
#         })

#     @http.route('/hta_sale_excel_report/hta_sale_excel_report/objects/<model("hta_sale_excel_report.hta_sale_excel_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_sale_excel_report.object', {
#             'object': obj
#         })
