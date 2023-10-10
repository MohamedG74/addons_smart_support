{
    'name': 'Custom Invoicing',
    'version': '16.0.0.0',
    'category': '',
    'summary': 'the voice',
    'description': """
    
    """,
    'author': 'SmartSupport',
    'website': 'https://www.smartsupport.tech',
    'depends': ['base','product','account'],
    'data': [
        'security/ir.model.access.csv',
        'views/invoicing.xml',
    ],

    'installable': True,
    'auto_install': False,
    "images": [],
}
