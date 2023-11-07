# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Smart - Stock Branches",
    "summary": "Adds the concept of branches in stock management",
    'author': "Smart Support",
    'website': "https://www.smartsupport.tech/",
    'category': 'Customizations',
    'version': '0.1',
    'application': True,
    'sequence': -99,
    "license": "LGPL-3",
    "depends": ["stock", "smart_multi_branch"],
    "data": ["security/stock_security.xml", "view/stock.xml"],#"data/stock_data.xml"
    "demo": [],
    "installable": True,
    #"post_init_hook": "update_operating_unit_location",
}
