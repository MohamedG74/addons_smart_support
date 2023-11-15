{
    'name': 'Add Status In Stock Picking',
    'version': '16.0.0.0',
    'category': '',
    'summary': '.',
    'description': """
      
""",
    'author': 'SmartSupport',
    'website': 'https://www.smartsupport.tech',
    'depends': ['base','account','project','purchase','sale'],
    'data': [
        'views/add_status.xml',
        'views/upload_file_purchase.xml',
        'views/upload_file_sales.xml',
    ],
    'js': [
        # 'static/src/js/custom_tree_script.js',
    ],
    'installable': True,
    'auto_install': False,
    "images":[],
}
