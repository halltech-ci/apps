# -*- coding: utf-8 -*-
# from odoo import http


# class WorkOrderRequest(http.Controller):
#     @http.route('/work_order_request/work_order_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/work_order_request/work_order_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('work_order_request.listing', {
#             'root': '/work_order_request/work_order_request',
#             'objects': http.request.env['work_order_request.work_order_request'].search([]),
#         })

#     @http.route('/work_order_request/work_order_request/objects/<model("work_order_request.work_order_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('work_order_request.object', {
#             'object': obj
#         })
