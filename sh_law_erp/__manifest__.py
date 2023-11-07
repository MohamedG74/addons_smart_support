# Part of Softhealer Technologies.
{
    "name": "Smart Law ERP",
    "author": "SmartSupport",
    "website": "https://www.smartsupport.tech",
    "support": "support@smartsupport.tech",
    "category": "Point of Sale",
    "summary": "",
    "description": """ Law ERP.  """,
    "version": "16.0.2",
    "depends": ["account", 'base','hr'],
    "application": True,
    "license": "OPL-1",
    "data": [
        'security/ir.model.access.csv',
        'security/sh_law_erp_security.xml',
        'reports/matter_detailed_report.xml',
    ],
    "images": [],
    "auto_install": False,
    "installable": True,
}
