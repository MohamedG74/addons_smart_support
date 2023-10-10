{
    'name': 'Maintenance Types',
    'version': '16.0.0.0',
    'category': '',
    'summary': '.',
    'description': """
      
""",
    'author': 'SmartSupport',
    'website': 'https://www.smartsupport.tech',
    'depends': ['base','account','maintenance','web_tour'],
    'data': [
        'for_security/ir.model.access.csv',    
        'views/maintenance.xml',
        'views/maintenance_locations.xml',
        'views/code.xml',
        
    ],
    'installable': True,
    'auto_install': False,
    "images":[],

    'assets': {
        'web.assets_backend': [
            # 'maintenance_types/static/src/js/date_picker.js',
        ],
},
}
