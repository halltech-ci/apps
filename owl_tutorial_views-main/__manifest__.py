{
    'name': "hta_workorder_request",

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
    'category': 'Warehouse Management',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock',
                'product',
                'project'
               ],

    # always loaded
    'data': [
#         #'security/ir.model.access.csv',
#         'views/views.xml',
#         'views/templates.xml',
#         'views/workorder_request_views.xml',
#         'views/workorder_request_menu.xml',
#         'views/project_views.xml',
#         #data
#         'data/workorder_ir_sequence.xml',
#         #report
#         'report/workorder_report.xml',
#         'report/workorder_request_report.xml',
        
    ],
    # only loaded in demonstration mode
#     'demo': [
#         'demo/demo.xml',
#     ],
}