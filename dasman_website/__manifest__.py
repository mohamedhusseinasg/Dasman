# -*- coding: utf-8 -*-
{
    'name': "Dasman Website",
    "author": "Ahmed Mokhtar",
    'version': "17.0.1.0.0",
    'live_test_url': "",
    'website':"",
    "images": ['static/description/main_screenshot.png'],
    'summary': "dasman_website",
    'description': "dasman_website",
    "license": "OPL-1",
    'depends': ['base','website'],
    'data': [
    	# security
    	'security/security.xml',
    	'security/ir.model.access.csv',
    	# data
    	"data/data.xml",
	# views
        'views/template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'category': "tools",
}
