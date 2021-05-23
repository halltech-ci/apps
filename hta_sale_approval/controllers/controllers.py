# -*- coding: utf-8 -*-
# from odoo import http


# class HtaSaleApproval(http.Controller):
#     @http.route('/hta_sale_approval/hta_sale_approval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_sale_approval/hta_sale_approval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_sale_approval.listing', {
#             'root': '/hta_sale_approval/hta_sale_approval',
#             'objects': http.request.env['hta_sale_approval.hta_sale_approval'].search([]),
#         })

#     @http.route('/hta_sale_approval/hta_sale_approval/objects/<model("hta_sale_approval.hta_sale_approval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_sale_approval.object', {
#             'object': obj
#         })
