# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    @api.model_create_multi
    def create(self, vals_list):
        ''' Store the initial standard price in order to be able to retrieve the cost of a product template for a given date'''
        templates = super(ProductTemplate, self).create(vals_list)
        if "create_product_product" not in self._context:
            templates._create_variant_ids()

        # This is needed to set given values to first variant after creation
        for template, vals in zip(templates, vals_list):
            related_vals = {}
            if vals.get('display_name'):
                related_vals['description_sale'] = vals['display_name']
            if vals.get('barcode'):
                related_vals['barcode'] = vals['barcode']
            if vals.get('default_code'):
                related_vals['default_code'] = vals['default_code']
            if vals.get('standard_price'):
                related_vals['standard_price'] = vals['standard_price']
            if vals.get('volume'):
                related_vals['volume'] = vals['volume']
            if vals.get('weight'):
                related_vals['weight'] = vals['weight']
            # Please do forward port
            if vals.get('packaging_ids'):
                related_vals['packaging_ids'] = vals['packaging_ids']
            if related_vals:
                template.write(related_vals)

        return templates

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    
    """@api.model_create_multi
    def create(self, vals_list):
        products = super(ProductProduct, self.with_context(create_product_product=True)).create(vals_list)
        # `_get_variant_id_for_combination` depends on existing variants
        if vals.get('product_variant_id'):
            related_vals['name'] = vals['product_variant_id']
        self.clear_caches()
        return products
    """
    
    def name_get(self):
        # TDE: this could be cleaned a bit I think

        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            if code:
                name = name
            return (d['id'], name)

        partner_id = self._context.get('partner_id')
        if partner_id:
            partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
        else:
            partner_ids = []
        company_id = self.env.context.get('company_id')

        # all user don't have access to seller and partner
        # check access and use superuser
        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []

        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        # Use `load=False` to not call `name_get` for the `product_tmpl_id`
        self.sudo().read(['name', 'default_code', 'product_tmpl_id'], load=False)

        product_template_ids = self.sudo().mapped('product_tmpl_id').ids

        if partner_ids:
            # name_get() of product with different quantities of the same supplier will be ambiguous, so
            # we can pass a supplier_info in the context if we already know which one we want
            supplier_info = self.env.context.get('supplier_info', False)
            if not supplier_info:
                supplier_info = self.env['product.supplierinfo'].sudo().search([
                    ('product_tmpl_id', 'in', product_template_ids),
                    ('name', 'in', partner_ids),
                ])
            # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
            # Use `load=False` to not call `name_get` for the `product_tmpl_id` and `product_id`
            supplier_info.sudo().read(['product_tmpl_id', 'product_id', 'product_name', 'product_code'], load=False)
            supplier_info_by_template = {}
            for r in supplier_info:
                supplier_info_by_template.setdefault(r.product_tmpl_id, []).append(r)
        for product in self.sudo():
            variant = product.product_template_attribute_value_ids._get_combination_name()

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            sellers = []
            if partner_ids:
                product_supplier_info = supplier_info_by_template.get(product.product_tmpl_id, [])
                sellers = [x for x in product_supplier_info if x.product_id and x.product_id == product]
                if not sellers:
                    sellers = [x for x in product_supplier_info if not x.product_id]
                # Filter out sellers based on the company. This is done afterwards for a better
                # code readability. At this point, only a few sellers should remain, so it should
                # not be a performance issue.
                if company_id:
                    sellers = [x for x in sellers if x.company_id.id in [company_id, False]]
            if sellers:
                for s in sellers:
                    seller_variant = s.product_name and (
                        variant and "%s (%s)" % (s.product_name, variant) or s.product_name
                        ) or False
                    mydict = {
                              'id': product.id,
                              'name': seller_variant or name,
                              'default_code': s.product_code or product.default_code,
                              }
                    temp = _name_get(mydict)
                    if temp not in result:
                        result.append(temp)
            else:
                mydict = {
                          'id': product.id,
                          'name': name,
                          'default_code': product.default_code,
                          }
                result.append(_name_get(mydict))
        return result
