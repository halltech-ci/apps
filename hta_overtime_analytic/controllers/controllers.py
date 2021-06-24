# -*- coding: utf-8 -*-
# from odoo import http


# class HtaOvertimeAnalytic(http.Controller):
#     @http.route('/hta_overtime_analytic/hta_overtime_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_overtime_analytic/hta_overtime_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_overtime_analytic.listing', {
#             'root': '/hta_overtime_analytic/hta_overtime_analytic',
#             'objects': http.request.env['hta_overtime_analytic.hta_overtime_analytic'].search([]),
#         })

#     @http.route('/hta_overtime_analytic/hta_overtime_analytic/objects/<model("hta_overtime_analytic.hta_overtime_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_overtime_analytic.object', {
#             'object': obj
#         })
