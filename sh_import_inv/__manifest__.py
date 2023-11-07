# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Import Invoice from CSV/Excel file",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Accounting",
    "summary": """import invoice from csv module, import invoice from excel, import bill from csv,import receipt from csv,import receipt from excel, import payment from csv, import payment from excel, import invoice from xls, impoer bill from xlsx odoo""",
    "description": """
 This module useful to import invoice from csv/excel. 
 import invoice from csv module, import invoice from excel, import bill from csv app, import receipt from csv, import receipt from excel, import payment from csv, import payment from excel, import invoice from xls xlsx, impoer bill from excel odoo

                    """,
    "version": "14.0.1",
    "depends": [
        "sh_message",
        "account"
    ],
    "application": True,
    "data": [
        'security/import_inv_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_inv_wizard.xml',
        'views/account_view.xml',
    ],
    'external_dependencies': {
        'python': ['xlrd'],
    },
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/uyHGc3ivazk",
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
