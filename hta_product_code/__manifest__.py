# -*- coding: utf-8 -*-
{
    'name': "hta_product_code",

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
    'category': 'Uncategorized',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['product_variant_default_code',
               #'stock',
               ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #"security/product_security.xml",
        'views/views.xml',
        'views/templates.xml',
        #views
        #'views/product_category_views.xml',
        #'views/product_views.xml',
        #"views/product_attribute_views.xml",
        #"views/config_settings_views.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
    "installable": True,
    #"pre_init_hook": "pre_init_product_category_code",
}
