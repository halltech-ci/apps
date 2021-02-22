# -*- coding: utf-8 -*-
# from odoo import http


# class HtaWorkorderRequest(http.Controller):
#     @http.route('/hta_workorder_request/hta_workorder_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_workorder_request/hta_workorder_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_workorder_request.listing', {
#             'root': '/hta_workorder_request/hta_workorder_request',
#             'objects': http.request.env['hta_workorder_request.hta_workorder_request'].search([]),
#         })

#     @http.route('/hta_workorder_request/hta_workorder_request/objects/<model("hta_workorder_request.hta_workorder_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_workorder_request.object', {
#             'object': obj
#         })
