{
    #  Information
    'name': 'ReportsTechultra',
    'version': '13.0.0.1',
    'summary': 'Reports for all',
    'description': 'Reports for all',
    'category': '',

    # Author
    'author': 'Techultra Solution',
    'website': 'https://www.techultrasolutions.com',
    'license': '',

    #  Depends
    'depends': ['sale_management', 'account', 'sale_stock', 'purchase'],
    'data': [
        'data/report_paperformat_data_tus.xml',
        'reports/all_action_reports_overrides.xml',
        'reports/report_saleorder_tus.xml',
        'reports/report_sale_quotations.xml',
        'reports/sale_delivery_notes.xml',
        'reports/sale_picking_operation.xml',
        'reports/sale_tax_invoice.xml',
        'reports/sale_credit_note.xml',
        'reports/purchase_order.xml',
        'reports/purchase_debit_note.xml',
        'reports/purchase_goods_receipt.xml',
        'reports/purchase_pre_forma_invoice.xml',
        'reports/purchase_tax_invoice.xml',
    ],

    #  Others
    'application': True,
    'installable': True,
    'auto_install': False,

}
