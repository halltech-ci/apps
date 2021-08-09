# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomReportPurchase(http.Controller):
#     @http.route('/hta_custom_report_purchase/hta_custom_report_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_report_purchase/hta_custom_report_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_report_purchase.listing', {
#             'root': '/hta_custom_report_purchase/hta_custom_report_purchase',
#             'objects': http.request.env['hta_custom_report_purchase.hta_custom_report_purchase'].search([]),
#         })

#     @http.route('/hta_custom_report_purchase/hta_custom_report_purchase/objects/<model("hta_custom_report_purchase.hta_custom_report_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_report_purchase.object', {
#             'object': obj
#         })
