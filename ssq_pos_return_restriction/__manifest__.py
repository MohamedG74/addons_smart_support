{
    "name": "Smart - POS Return Restriction",
    "summary": """Employee wise return restriction in POS""",
    "description": """
        In Odoo Point of Sale, currently there are no restriction in the case of returns.
        This module will bring in a restriction in the case of returns. The employees who can do the
        returns should be selected in each POS shop configuration.
    """,
    "author": "Smart Support",
    "website": "https://www.smartsupport.tech/",
    "support": "info@smartsupport.tech",
    "license": "OPL-1",
    "category": "Sales/Point of Sale",
    "version": "15.4",
    "depends": ["pos_hr","sales_team","hr","point_of_sale","pos_settle_due"],
    "images": ["static/description/pos_return_restriction_v15.png"],
    "data": [
        #"views/pos_config_view.xml",
        "views/target.xml",
        "views/employee.xml",
        "views/product_template.xml"
    ],
    "assets": {
        'web.assets_qweb': [
          #  'ssq_pos_return_restriction/views/OrderReceipt.xml',
        ],
        "point_of_sale.assets": [
           # "/ssq_pos_return_restriction/static/src/js/ProductScreen.js",
        ],
    },
    'auto_install': True,
    'application': True,
    'sequence': -97,
}
