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
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_holidays',
               'hr_payroll',
               'account',
               'hr_payroll_account',
               'project',
               'report_xlsx',
               ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #security
        'security/hr_payslip_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/hr_contract_views.xml',
        #'views/hr_payslip_views.xml',
        'views/hr_employee_views.xml',
        'views/account_paybook_report.xml',
        'views/hr_work_entry_type_views.xml',
        'views/hr_salary_rule_views.xml',
        'views/template_css.xml',
        #Report
        'report/report_hta_payslip_template.xml',
        'report/bulletin_paye_report.xml',
        'report/paybook_template.xml',
        'report/paybook_xlsx_report.xml',
        'wizard/paybook_excel_wizard.xml',
        
        #Data
        'data/hta_hr_payroll_data.xml',
        #'data/hta_hr_leave_type.xml',
    ],
    'css': ['static/src/css/my_css.css'],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
