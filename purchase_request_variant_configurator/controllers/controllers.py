# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseRequestVariantConfigurator(http.Controller):
#     @http.route('/purchase_request_variant_configurator/purchase_request_variant_configurator/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_request_variant_configurator/purchase_request_variant_configurator/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_request_variant_configurator.listing', {
#             'root': '/purchase_request_variant_configurator/purchase_request_variant_configurator',
#             'objects': http.request.env['purchase_request_variant_configurator.purchase_request_variant_configurator'].search([]),
#         })

#     @http.route('/purchase_request_variant_configurator/purchase_request_variant_configurator/objects/<model("purchase_request_variant_configurator.purchase_request_variant_configurator"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_request_variant_configurator.object', {
#             'object': obj
#         })
