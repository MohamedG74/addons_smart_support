# Part of Softhealer Technologies.
{
    "name": "Smart Restrict POS Stock",
    "author": "SmartSupport",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point of Sale",
    "summary": "",
    "description": """ Restrict Stock.  """,
    "version": "16.0.2",
    "depends": ["point_of_sale","pos_discount", 'utm', "portal", "pos_hr", "purchase"],
    "application": True,
    "license": "OPL-1",
    "data": [
        'views/res_pos_config.xml',
        'views/pos_order.xml',

        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/stock_quant_views.xml',

        'views/stock_move_history.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'restrict_pos_stock/static/src/js/Screens/ProductScreen.js',
            'restrict_pos_stock/static/src/js/Screens/NumpadWidget.js',

            'restrict_pos_stock/static/src/js/Screens/TicketScreen.js',
            'restrict_pos_stock/static/src/js/Screens/PartnerLine.js',
            'restrict_pos_stock/static/src/js/Screens/PartnerListScreen.js',
            'restrict_pos_stock/static/src/js/Screens/OrderSummary.js',

            'restrict_pos_stock/static/src/xml/screens/OrderLine.xml',
            'restrict_pos_stock/static/src/xml/screens/ProductItem.xml',
            'restrict_pos_stock/static/src/xml/screens/ProductInfoPopup.xml',
            'restrict_pos_stock/static/src/xml/screens/TicketScreen.xml',
            'restrict_pos_stock/static/src/xml/screens/PartnerLine.xml',
            'restrict_pos_stock/static/src/xml/screens/OrderSummary.xml',
            'restrict_pos_stock/static/src/xml/screens/OrderWidget.xml',
            'restrict_pos_stock/static/src/xml/screens/OrderDetails.xml',
            'restrict_pos_stock/static/src/xml/screens/ReceiptScreen.xml',
            'restrict_pos_stock/static/src/xml/screens/Chrome.xml',
            'restrict_pos_stock/static/src/xml/screens/pos_fields.xml',

            'restrict_pos_stock/static/src/css/pos.scss',

            # pos secondary selling unit
            'restrict_pos_stock/static/pos_secondary/static/src/js/ControlButton/ChangeUOMButton.js',
            'restrict_pos_stock/static/pos_secondary/static/src/js/Screens/ProductItem.js',
            'restrict_pos_stock/static/pos_secondary/static/src/js/models.js',
            'restrict_pos_stock/static/pos_secondary/static/src/xml/ControlButton/ChangeUOMButton.xml',
            'restrict_pos_stock/static/pos_secondary/static/src/xml/OrderLinesReceipt.xml',

            # pos Note
            'restrict_pos_stock/static/sh_pos_note/static/src/scss/pos.scss',
            'restrict_pos_stock/static/sh_pos_note/static/src/js/Popups/popup.js',
            'restrict_pos_stock/static/sh_pos_note/static/src/js/Screens/screen.js',
            'restrict_pos_stock/static/sh_pos_note/static/src/js/action_button.js',
            'restrict_pos_stock/static/sh_pos_note/static/src/js/linebutton.js',
            'restrict_pos_stock/static/sh_pos_note/static/src/js/models.js',
            'restrict_pos_stock/static/sh_pos_note/static/src/xml/Popups/popup.xml',
            'restrict_pos_stock/static/sh_pos_note/static/src/xml/Screens/screen.xml',
            'restrict_pos_stock/static/sh_pos_note/static/src/xml/action_button.xml',
            'restrict_pos_stock/static/sh_pos_note/static/src/xml/receipt.xml',


        ],
         'web.assets_backend': [
            'restrict_pos_stock/static/src/css/pos.scss'
         ]
    },
    "images": [],
    "auto_install": False,
    "installable": True,
}
