{
    'name': 'Maintenance Types',
    'version': '16.0.0.0',
    'category': '',
    'summary': '.',
    'description': """
      
""",
    'author': 'SmartSupport',
    'website': 'https://www.smartsupport.tech',
    'depends':['base', 'maintenance'],
    'data':[
        'security/ir.model.access.csv',
        'views/mainten.xml',
        'views/location.xml',
        'views/request.xml',
        
        
    ],
    'installable': True,
    'auto_install': True,
    'application':True,

}