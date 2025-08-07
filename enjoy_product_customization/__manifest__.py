# -*- coding: utf-8 -*-
{
    'name': "Enjoy Product Customization",
    "author": "Ahmed Mokhtar",
    'version': "17.0.1.1.1",
    'live_test_url': "",
    'website':"",
    "images": ['static/description/main_screenshot.png'],
    'summary': "enjoy_product_customization",
    'description': "enjoy_product_customization",
    "license": "OPL-1",
    'depends': ['base','product','stock'],
    'data': [
    	# security
    	# 'security/security.xml',
    	'security/ir.model.access.csv',
    	# data
    	# "data/data.xml",
	# views
        'views/product_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'category': "product",
}
