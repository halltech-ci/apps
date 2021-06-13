# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomOvertime(http.Controller):
#     @http.route('/hta_custom_overtime/hta_custom_overtime/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_overtime/hta_custom_overtime/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_overtime.listing', {
#             'root': '/hta_custom_overtime/hta_custom_overtime',
#             'objects': http.request.env['hta_custom_overtime.hta_custom_overtime'].search([]),
#         })

#     @http.route('/hta_custom_overtime/hta_custom_overtime/objects/<model("hta_custom_overtime.hta_custom_overtime"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_overtime.object', {
#             'object': obj
#         })
