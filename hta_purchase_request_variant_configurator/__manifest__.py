# -*- coding: utf-8 -*-
{
    'name': "hta_purchase_request_variant_configurator",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase Management',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase_request_custom',
               "product_variant_configurator",
               ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        "views/purchase_request_form_views.xml",
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
    "installable": True,
    "post_init_hook": "assign_product_template",
}
