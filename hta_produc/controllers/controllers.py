# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProduc(http.Controller):
#     @http.route('/hta_produc/hta_produc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_produc/hta_produc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_produc.listing', {
#             'root': '/hta_produc/hta_produc',
#             'objects': http.request.env['hta_produc.hta_produc'].search([]),
#         })

#     @http.route('/hta_produc/hta_produc/objects/<model("hta_produc.hta_produc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_produc.object', {
#             'object': obj
#         })
