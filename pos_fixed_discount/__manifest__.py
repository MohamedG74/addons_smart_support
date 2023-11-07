# Copyright 2020 Lorenzo Battistini @ TAKOBI
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Smart - Point of Sale Fixed Discounts",
    "summary": "Allow to apply discounts with fixed amount",
    "version": "15.5",
    'author': "Smart Support",
    'website': "https://www.smartsupport.tech/", 
    "category": "Point of Sale",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["point_of_sale","pos_discount","account"],
    'data': [
        'views/after.xml',
        #'views/pos_templates.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_fixed_discount/static/src/js/**/*',
            'pos_fixed_discount/static/src/xml/**/*',
        ],
    },
    'qweb': [
        'static/src/xml/discount_templates.xml',
    ],
}
