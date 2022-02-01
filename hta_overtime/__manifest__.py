# -*- coding: utf-8 -*-
{
    'name': "hta_overtime",

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
    'category': 'Human Resources/Overtimes',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr', 
                'calendar', 
                'resource',
               ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/hta_overtime_security.xml',
        #views
        'views/hta_overtime_views.xml',
        'views/hta_overtime_menu.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
