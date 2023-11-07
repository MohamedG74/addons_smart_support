{
    'name': "POS Credit Limit",
    'version': '16.01.0.0   ',
    'depends': ['base', 'sale_management', 'contacts'],
    'author': "David Dazzil",
    'category': 'Category',
    'description': "Sale Order Credit Limit",
    'application': True,
    # data files always loaded at installation

    'assets': {
        'point_of_sale.assets': [
            #'/pos_credit_limit/static/src/xml/partner_pos.xml',
            #'/pos_credit_limit/static/src/xml/partner_line_pos.xml',
            '/pos_credit_limit/static/src/js/partner_pos.js',
            # '/spanish_pos/static/src/xml/product_view_pos.xml',
        ],
        # 'web.assets_backend': [
        #     '/spanish_pos/static/src/js/receipt_pos.js',
        #     '/spanish_pos/static/src/js/product_view_pos.js',
        # ],
    },

    'data': [
       # 'view/credit_journal.xml',
        'view/credit_partner.xml',
        # 'security/ir.model.access.csv',
    ],
}
