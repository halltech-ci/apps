# -*- coding: utf-8 -*-
{
    'name': "custom_apps",

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
    'depends': ['hta_custom_sale',
                #'sale_order_secondary_unit',
                ],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/account_cash_views.xml',
        #'views/account_analytic_tag_views.xml',
        'views/account_move_views.xml',
        'views/account_account_views.xml',
        'views/project_views.xml',
        #'views/sale_order_views.xml',
        #data sequence
        'data/sale_ir_sequence.xml',
        'data/purchase_ir_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
