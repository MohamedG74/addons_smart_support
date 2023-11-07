# -*- coding: utf-8 -*-
# Copyright (C) 2022-Today Henderson Zambrano <zambranohender@gmail.com>


{
    'name': 'Smart - Point of Sale Require Customer',
    'version': '15.0.1.0.0',
    'category': 'Point Of Sale',
    'summary': 'Point of Sale Require Customer',
    'author': "Smart Support",
    'website': "https://www.smartsupport.tech/", 
    'depends': ['point_of_sale'],
    'data': [

        'views/pos_config_view.xml',
   
    ],
    'assets': {
        'point_of_sale.assets': [
            '/pos_customer_required/static/src/js/PaymentScreen.js',

        ],   
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
