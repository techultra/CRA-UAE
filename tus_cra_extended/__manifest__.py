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
    'depends': ['purchase', 'hr_contract'],
    'external_dependencies': {},
    'data': [
        'views/res_users.xml',
        'views/purchase_order_line.xml',
        'views/hr_contract.xml',
        'views/hr_employee.xml',
        'wizards/gratuity.xml',
        'reports/report_action.xml',
        'reports/gratuity_report.xml',
    ],

    #  Others
    'application': True,
    'installable': True,
    'auto_install': False,

}
