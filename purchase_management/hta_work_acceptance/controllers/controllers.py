# -*- coding: utf-8 -*-
# from odoo import http


# class HtaWorkAcceptance(http.Controller):
#     @http.route('/hta_work_acceptance/hta_work_acceptance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_work_acceptance/hta_work_acceptance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_work_acceptance.listing', {
#             'root': '/hta_work_acceptance/hta_work_acceptance',
#             'objects': http.request.env['hta_work_acceptance.hta_work_acceptance'].search([]),
#         })

#     @http.route('/hta_work_acceptance/hta_work_acceptance/objects/<model("hta_work_acceptance.hta_work_acceptance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_work_acceptance.object', {
#             'object': obj
#         })
