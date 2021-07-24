# -*- coding: utf-8 -*-
# from odoo import http


# class HtaPurchaseRequestVariantConfigurator(http.Controller):
#     @http.route('/hta_purchase_request_variant_configurator/hta_purchase_request_variant_configurator/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_purchase_request_variant_configurator/hta_purchase_request_variant_configurator/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_purchase_request_variant_configurator.listing', {
#             'root': '/hta_purchase_request_variant_configurator/hta_purchase_request_variant_configurator',
#             'objects': http.request.env['hta_purchase_request_variant_configurator.hta_purchase_request_variant_configurator'].search([]),
#         })

#     @http.route('/hta_purchase_request_variant_configurator/hta_purchase_request_variant_configurator/objects/<model("hta_purchase_request_variant_configurator.hta_purchase_request_variant_configurator"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_purchase_request_variant_configurator.object', {
#             'object': obj
#         })
