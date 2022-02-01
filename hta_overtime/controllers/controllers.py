# -*- coding: utf-8 -*-
# from odoo import http


# class HtaOvertime(http.Controller):
#     @http.route('/hta_overtime/hta_overtime/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_overtime/hta_overtime/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_overtime.listing', {
#             'root': '/hta_overtime/hta_overtime',
#             'objects': http.request.env['hta_overtime.hta_overtime'].search([]),
#         })

#     @http.route('/hta_overtime/hta_overtime/objects/<model("hta_overtime.hta_overtime"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_overtime.object', {
#             'object': obj
#         })
