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
    'depends': ['purchase'],
    'external_dependencies': {},
    'data': [
        'views/res_users.xml',
        'views/purchase_order_line.xml',
    ],

    #  Others
    'application': True,
    'installable': True,
    'auto_install': False,

}
