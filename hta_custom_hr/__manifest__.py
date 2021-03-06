# -*- coding: utf-8 -*-
{
    'name': "hta_custom_hr",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '10.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
               'hr_payroll',
               'account',
               'hr_payroll_account',
               'project',
               #'hr_timesheet_sheet',
               ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/hr_employee_views.xml',
        #'views/hr_payslip_views.xml',
        'report/report_hta_payslip_template.xml',
        'report/bulletin_paye_report.xml',
        #'report/payslip_book.xml',
        'report/payslip_reporting_template.xml',
        'report/report_payslip_book.xml',
        'wizard/payslip_reporting_book.xml',
        'views/hr_contract_views.xml',
        'views/hr_attendance_views.xml',
        'data/hta_hr_payroll_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}