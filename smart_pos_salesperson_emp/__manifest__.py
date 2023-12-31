# -*- coding: utf-8 -*-
{
    'name': 'Smart - POS Salesperson',
    'version': '1.0',
    'author': 'Smart Support',
    'category': 'Point of Sale',
    'depends': ['point_of_sale', 'hr'],
    'summary': 'This apps helps you set salesperson on pos orderline from pos interface | POS Orderline User | Assign Sales Person on POS | POS Sales Person',
    'description': """
- Odoo POS Orderline user
- Odoo POS Orderline salesperson
- Odoo POS Salesperson
- Odoo POS Item Salesperson
- Odoo POS Item User
- Odoo POS product salesperson
    """,
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'smart_pos_salesperson_emp/static/src/js/**/*',
            'smart_pos_salesperson_emp/static/src/xml/**/*',
        ],
    },
    'price': 40.0,
    'currency': "EUR",
    'application': True,
    'installable': True,
    "license": "LGPL-3",
    "images":[],
}
