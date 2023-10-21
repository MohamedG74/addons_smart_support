{
    'name': 'Learn js',
    'version': '16.0.0.0',
    'category': '',
    'summary': '.',
    'description': """
      
""",
    'author': 'SmartSupport',
    'website': 'https://www.smartsupport.tech',
    'depends':['base','point_of_sale'],
    'data':[
        
    ],

    'assets':{

    # 'web.assets_qweb': [
    #       'wb_portal/static/src/js/wb_sample_button.xml',
    #     ],
        'point_of_sale.assets':[
          'wb_portal/static/src/xml/wb_sample_button.xml',
          'wb_portal/static/src/js/wb_sample_button.js',
        ]
    }
    

}