{
    "name": "Smart - Multi Branch",
    'summary': """
         Allow Making Branches and link with other apps. 
         """,

    'description': """
        Allow Making Branches and link with other apps. 
    """,

    'author': "Smart Support",
    'website': "https://www.smartsupport.tech/",
    'category': 'Customizations',
    'version': '0.1',
    'application': True,
    'sequence': -99,
    "depends": ["base"],
    "license": "LGPL-3",
    "data": [
        "security/branch_security.xml",
        "security/ir.model.access.csv",
        "data/branch_data.xml",
        "view/branch_view.xml",
        "view/res_users_view.xml",
    ],
    "demo": ["demo/branch_demo.xml"],
    "installable": True,
}
