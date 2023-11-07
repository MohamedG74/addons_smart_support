# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Import Product Template from CSV/Excel file",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Productivity",
    "summary": "import product Template from csv, import product Template from excel, import Template from csv, import product Template from xls, import product Template from xlsx odoo",
    "description": """This module is useful to product template with from CSV/Excel file. You can import custom fields from CSV or Excel.
 Import Product Template From CSV , Import Product Template From excel Odoo
 Import Template From CSV Module, Import Template From Excel, Import Template From XLS XLSX Odoo.
 Import Template From CSV Module, Import Template From Excel App, import Template From XLS XLSX Odoo .
 Importar plantilla de producto desde CSV, Importar plantilla de producto desde Excel Odoo
Importar plantilla desde módulo CSV, Importar plantilla desde Excel, Importar plantilla desde XLS XLSX Odoo.
Importar plantilla del módulo CSV, Importar plantilla de la aplicación Excel, importar plantilla de XLS XLSX Odoo.""",
    "version": "14.0.1",
    "depends": [
        "sale_management",
        "stock",
        "sh_message",
    ],
    "application": True,
    "data": [
        'security/import_product_tmpl_security.xml',
        'security/ir.model.access.csv',
        'wizard/import_product_tmpl_wizard.xml',
        'views/sale_view.xml',
    ],
    'external_dependencies': {
        'python': ['xlrd'],
    },
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/Qyuv3j1LTKI",
    "license": "OPL-1",
    "auto_install": False,
    "installable": True,
    "price": 25,
    "currency": "EUR"
}
