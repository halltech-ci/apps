# -*- coding: utf-8 -*-
# from odoo import http


# class HtaAnalyticReport(http.Controller):
#     @http.route('/hta_analytic_report/hta_analytic_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_analytic_report/hta_analytic_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_analytic_report.listing', {
#             'root': '/hta_analytic_report/hta_analytic_report',
#             'objects': http.request.env['hta_analytic_report.hta_analytic_report'].search([]),
#         })

#     @http.route('/hta_analytic_report/hta_analytic_report/objects/<model("hta_analytic_report.hta_analytic_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_analytic_report.object', {
#             'object': obj
#         })
