# Copyright (C) Softhealer Technologies.

{
    "name": "POS Total Items Count",
    "version": "16.0.1",
    "category": "Point of Sale",
    "license": "OPL-1",
    "depends": ['base', 'sale', 'point_of_sale'],
    'author': 'Softhealer Technologies',
    'website': 'https://www.softhealer.com',
    "support": "support@softhealer.com",
    'summary': "POS Items Counter, Point Of Sale Product Counter, POS Total Item Count, Point Of Sale Item Calculate, POS Product Count App, POS Item Counter Module, POS Item Management, Point Of Sale Total Product Odoo",
    "description": """ In Point of Sale, it is necessary to count the number of items for a particular order. This module shows you the number of products in the POS cart & POS Receipt. """,
    "data": [
        'views/res_config_settings.xml'
    ],
    'assets': {
                'point_of_sale.assets': [
                                        'sh_pos_counter/static/src/js/counter.js',
                                        'sh_pos_counter/static/src/css/pos.css',
                                        'sh_pos_counter/static/src/xml/order_summary.xml',
                                        'sh_pos_counter/static/src/xml/order_receipt.xml'
                                        ],
               
               },
    "images": ['static/description/background.png'],
    "live_test_url": "https://youtu.be/WeefGz5JyJ0",
    "auto_install": False,
    "installable": True,
    "price": 15,
    "currency": 'EUR',
}
