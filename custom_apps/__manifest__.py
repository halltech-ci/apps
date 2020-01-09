# -*- coding: utf-8 -*-
{
    'name': "custom_apps",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Halltech Africa",
    'website': "http://www.halltech-africa.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchases',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
               'purchase',
                'project',
                'sale_management'
               ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/project_views.xml',
        'views/product_template_views.xml',
        'views/purchase_order_report.xml',
        'views/sale_views.xml',
        'views/sale_order_report.xml',
        'data/project_ir_sequence.xml',
        #'data/sale_ir_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}