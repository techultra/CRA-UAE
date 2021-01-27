{
    #  Information
    'name': 'Modified Reports',
    'version': '13.0',
    'summary': '',
    'description': 'Modification in base reports',
    'category': '',

    # Author
    'author': 'TechUltra Solution',
    'website': 'https://www.techultrasolutions.com',
    'license': '',

    #  Depends
    'depends': ['purchase', 'hr_contract', 'hr_payroll'],
    'external_dependencies': {},
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/menu_access_rights.xml',
        'views/res_users.xml',
        'views/purchase_order_line.xml',
        'views/hr_contract.xml',
        'views/hr_employee.xml',
        'views/hr_payslip.xml',
        'wizards/gratuity.xml',
        'wizards/pay_slip_view.xml',
        'reports/hr_leave_type.xml',
        'reports/report_action.xml',
        'reports/gratuity_report.xml',
    ],

    #  Others
    'application': True,
    'installable': True,
    'auto_install': False,

}
