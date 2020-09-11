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
    'depends': ['account', 'stock', 'sale_management'],
    'external_dependencies': {},
    'data': [
        'reports/stock_picking_operation.xml',
        'reports/delivery_notes.xml',
        'reports/invoice.xml',
    ],

    #  Others
    'application': True,
    'installable': True,
    'auto_install': False,

}
