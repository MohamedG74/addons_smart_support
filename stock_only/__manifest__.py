# Part of Softhealer Technologies.
{
    "name": "Smart Stock Only",
    "author": "SmartSupport",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point of Sale",
    "summary": "cash in cash out own customer discount mass update product tags own product template auto validate pos quick print receipt import pos secondary product suggestion pos access right pos auto lock cancel whatsapp return exchange pos all feature Restaurant & Shop Retail All In One POS Enterprise POS Community All In One POS all in one features pos Reorder pos Reprint pos Coupon Discount pos Order Return pos order all pos all features pos discount pos order list print pos receipt pos item count retail pos retail import sale from pos create quote from pos odoo All in one pos Reprint pos Return POS Stock pos gift import sale from pos pos multi currency payment pos pay later pos internal transfer pos disable payment pos product template pos product operation pos loyalty rewards all pos reports pos stock pos retail pos label pos cash control pos cash in out pos cash out pos logo pos receipt all pos in one all pos in one retail  odoo",
    "description": """ This is the fully retail solution for any kind of retail shop or bussiness.  """,
    "version": "16.0.2",
    "depends": ["point_of_sale", 'utm', "portal", "pos_hr", "purchase"],
    "application": True,
    "license": "OPL-1",
    "data": [
        # Responsive theme        
        'security/ir.model.access.csv',
        #'data/sh_pos_theme_responsive/pos_theme_settings_data.xml',
        'views/res_pos_config.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            
            #"stock_only/static/sh_pos_theme_responsive/static/src/scss/pos_theme_variables.scss",
            #'stock_only/static/sh_pos_theme_responsive/static/src/scss/fonts.scss',
            #'stock_only/static/sh_pos_theme_responsive/static/src/scss/pos_theme.scss',
            #'stock_only/static/sh_pos_theme_responsive/static/src/scss/pos.scss',
            #'stock_only/static/sh_pos_theme_responsive/static/src/css/*',
            #'stock_only/static/sh_pos_theme_responsive/static/src/js/**/*',
            #'stock_only/static/sh_pos_theme_responsive/static/src/xml/**/*',

             # POS Product Warehouse Qty
            'stock_only/static/src/js/db.js',
            'stock_only/static/src/js/models.js',
            'stock_only/static/src/js/popups/ProductQtyPopup.js',
            'stock_only/static/src/js/popups/QuantityWarningPopup.js',
            'stock_only/static/src/js/Screens/PaymentScreen.js',
            'stock_only/static/src/js/Screens/ProductScreen.js',
            'stock_only/static/src/js/Screens/ProductsWidget.js',
            'stock_only/static/src/js/Screens/TicketScreen.js',
            'stock_only/static/src/scss/pos.scss',
            'stock_only/static/src/xml/popups/ProductQtyPopup.xml',
            'stock_only/static/src/xml/popups/QuantityWarningPopup.xml',
            'stock_only/static/src/xml/screens/ProductItem.xml',
            'stock_only/static/src/xml/Orderline.xml'

            'stock_only/static/sh_pos_wh_stock_adv/static/src/js/screeen/PaymentScreen.js',
            'stock_only/static/sh_pos_wh_stock_adv/static/src/js/chrome.js',
            'stock_only/static/sh_pos_wh_stock_adv/static/src/js/models.js',

        ]
    },
    "images": [],
    "auto_install": False,
    "installable": True,
}