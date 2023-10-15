{
    'name': 'Hospital Management System',
    'version': '16.0.0.0',
    'category': '',
    'summary': '.',
    'description': """
      
""",
    'author': 'SmartSupport',
    'website': 'https://www.smartsupport.tech',
    'depends':['mail'],
    'data':[
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/pateint.xml',
        'views/doctor.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application':True,

}