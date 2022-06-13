# -*- coding: utf-8 -*-
{
    'name': "hta_purchase_type",

    'summary': """
        Define type of purchase request. Purchase request has different type: it can be for project, for asset or for stock""",

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
    'depends': ['purchase_request'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/purchase_type_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
