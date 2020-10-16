# -*- coding: utf-8 -*-
from odoo import http

# class HtaAssetManagement(http.Controller):
#     @http.route('/hta_asset_management/hta_asset_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_asset_management/hta_asset_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_asset_management.listing', {
#             'root': '/hta_asset_management/hta_asset_management',
#             'objects': http.request.env['hta_asset_management.hta_asset_management'].search([]),
#         })

#     @http.route('/hta_asset_management/hta_asset_management/objects/<model("hta_asset_management.hta_asset_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_asset_management.object', {
#             'object': obj
#         })