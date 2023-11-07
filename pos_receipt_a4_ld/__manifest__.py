# -*- coding: utf-8 -*-
# Part of Lebowski. See LICENSE file for full copyright and licensing details.

{
    'name': 'Smart - Pos Receipt A4',
    'version': '1.3',
    'sequence': 3,
    'author': "Smart Support",
    'website': "https://www.smartsupport.tech/", 
    'license': 'OPL-1',
    'category': 'Sales/Point of Sale',
    'summary': 'Elegant A4 Pos Receipt ',
    'description': """
    Print A4 receipt inside POS
    ===========================
    
    Option to print A4 receipt alongside your old receipt
    Option to set A4 receipt as the default receipt
    Option to render Barcode or Qrcode code in A4 receipt
    
    """,
    'depends': ['point_of_sale'],
    'data': [
        #'views/assets.xml',
        'views/pos_config_view.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
        'static/src/xml/postwo.xml',        
    ],
    'assets' : {
        'point_of_sale.assets': [
            'pos_receipt_a4_ld/static/src/css/posfinal.css',
            'pos_receipt_a4_ld/static/lib/JsBarcode.all.min.js',
            'pos_receipt_a4_ld/static/lib/qrcode.min.js',
            'pos_receipt_a4_ld/static/src/js/Barcode.js',
            'pos_receipt_a4_ld/static/src/js/Qrcode.js',
            'pos_receipt_a4_ld/static/src/js/AmountInWords.js',
            'pos_receipt_a4_ld/static/src/js/OrderReceiptA4.js',
            'pos_receipt_a4_ld/static/src/js/OrderReceiptA4Two.js',
            'pos_receipt_a4_ld/static/src/js/ReceiptScreen.js',
            'pos_receipt_a4_ld/static/src/js/ReprintReceiptScreen.js',
            'pos_receipt_a4_ld/static/src/js/DefaultCode.js',
            'pos_receipt_a4_ld/static/src/js/ClientData.js',
            
        ],
        'web.assets_qweb': [
            'pos_receipt_a4_ld/static/src/xml/**/*',
        ]
    },
    "images": ['static/description/thumbnail.gif'],
    'application': True,
    'installable': True,
}
