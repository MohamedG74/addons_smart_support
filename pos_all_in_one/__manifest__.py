# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "POS All in one -Advance Point of Sale All in one Features for retail",
    "version" : "15.0.0.8",
    "category" : "Point of Sale",
    'summary': 'All in one pos Reprint pos Return POS Stock pos gift import sale from pos pos multi currency payment pos pay later pos internal transfer pos disable payment pos product template pos product operation pos loyalty rewards all pos reports pos stock pos retail',
    "description": """
    
  POS all in one -  advance app features pos Reorder pos Reprint pos Coupon Discount pos Order Return POS Stock pos gift pos order all pos all features pos discount pos order list print pos receipt pos item count pos bag charges import sale from pos create quote from pos pos multi currency payment  pos pay later pos internal transfer pos discable payment pos product template pos product create/update pos loyalty rewards pos reports
    
    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 65,
    "currency": 'EUR',
    "depends" : ['base','sale_management','point_of_sale','pos_hr'],
    "data": [
        'security/ir.model.access.csv',
        'views/pos_loyalty.xml',
        'views/res_pos_config.xml',
    ],
    'qweb': [
    ],
    "auto_install": False,
    'license': 'OPL-1',
    "installable": True,
    'assets': {
        'point_of_sale.assets': [
           
            # # Add custom js for pos_loyalty

            "pos_all_in_one/static/src/js/loyalty_pos.js",
            "pos_all_in_one/static/src/js/OrderWidgetExtended.js",
            "pos_all_in_one/static/src/js/LoyaltyButtonWidget.js",
            "pos_all_in_one/static/src/js/LoyaltyPopupWidget.js",
            'pos_all_in_one/static/src/xml/pos_loyalty.xml',

            # Pos Order list 
            'pos_all_in_one/static/sh_pos_order_list/static/src/lib/jquery.simplePagination.js',
            'pos_all_in_one/static/sh_pos_order_list/static/src/js/ActionButtons/OrderHistoryButton.js',
            'pos_all_in_one/static/sh_pos_order_list/static/src/js/screens/OrderListScreen.js',
            'pos_all_in_one/static/sh_pos_order_list/static/src/js/screens/PaymentScreen.js',
            'pos_all_in_one/static/sh_pos_order_list/static/src/js/db.js',
            'pos_all_in_one/static/sh_pos_order_list/static/src/js/models.js',
            'pos_all_in_one/static/sh_pos_order_list/static/src/scss/pos.scss',
            'pos_all_in_one/static/sh_pos_order_list/static/src/scss/simplePagination.scss',
            'pos_all_in_one/static/sh_pos_order_list/static/src/xml/ActionButtons/OrderHistoryButton.xml',
            'pos_all_in_one/static/sh_pos_order_list/static/src/xml/screens/OrderListScreen.xml',

            # Pos Order Return/Exchange 
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/js/Popups/ReturnOrderPopup.js',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/js/screens/OrderListScreen.js',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/js/screens/PaymentScreen.js',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/js/db.js',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/js/Models.js',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/scss/pos.scss',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/xml/receipt.xml',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/xml/ReturnOrderPopup.xml',
            'pos_all_in_one/static/sh_pos_order_return_exchange/static/src/xml/screen.xml',



        ],
        'web.assets_qweb': [
        ],
    },
    "live_test_url":'https://youtu.be/3UcvG6ukjZE',
    "images":["static/description/Banner.png"],
}
