# -*- coding: utf-8 -*-
{
    'name': "Smart - Custom Reports",
    'summary': """Smart Support Custom Reports""",
    'description': """
        Smart Support Custom Reports
    """,
    'author': 'Smart Support.',
    'website': "https://www.smartsupport.tech/",
    'license': 'LGPL-3',
    'category': 'Customizations',
    'support': 'support@smartsupport.tech',
    'version': '15.0.1.0.0',
    'images': [],
    'depends': ['purchase','sale','base'],
    'data': [
        'views/sale_order.xml',
        'security/ir.model.access.csv',
    ],
    # 'qweb': ['static/src/xml/report.xml'],

    'assets' : {
        'web.assets_backend': [
            # 'smart_custom_report/static/src/css/**/*',
            'smart_custom_report/static/src/xml/**/*',
            'smart_custom_report/static/src/js/**/*',
        ],
    }
}
