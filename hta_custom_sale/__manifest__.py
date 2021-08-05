# -*- coding: utf-8 -*-
{
    'name': "hta_custom_sale",

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
    'category': 'Sale Management',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale_order_general_discount',
               'hta_custom_project','sign',
               ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        #views
        'views/sale_order_views.xml',
        #data
        'data/sale_ir_sequence.xml',
        #Reports
        'reports/sale_order_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
