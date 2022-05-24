# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomMrp(http.Controller):
#     @http.route('/hta_custom_mrp/hta_custom_mrp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_mrp/hta_custom_mrp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_mrp.listing', {
#             'root': '/hta_custom_mrp/hta_custom_mrp',
#             'objects': http.request.env['hta_custom_mrp.hta_custom_mrp'].search([]),
#         })

#     @http.route('/hta_custom_mrp/hta_custom_mrp/objects/<model("hta_custom_mrp.hta_custom_mrp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_mrp.object', {
#             'object': obj
#         })
