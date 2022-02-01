# -*- coding: utf-8 -*-
{
    'name': "purchase_request_custom",

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
    'depends': ['uom', 'purchase_request',
                #'custom_apps',
                'hta_custom_sale',
                'mail',
                'contacts',
                'hta_document_sign',
               ],

    # always loaded
    'data': [
        'security/purchase_request_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/purchase_request_views.xml',
        'views/purchase_request_line_views.xml',
        #"views/inherit_purchase_request_views.xml",
        "report/purchase_request_report.xml",
        "report/purchase_request_custom_report.xml",
        'report/purchase_order_custom_report.xml',
        #'data/mail_template_data.xml'
        #data
        'data/purchase_request_sequence.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
