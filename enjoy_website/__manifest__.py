# -*- coding: utf-8 -*-
{
    "name": "Dasman Website",
    "author": "Ahmed Mokhtar",
    "version": "17.0.1.0.0",
    "live_test_url": "",
    "website": "",
    "images": ["static/description/main_screenshot.png"],
    "summary": "dasman_website",
    "description": "dasman_website",
    "license": "OPL-1",
    "depends": ["base", "website", "stock", "website_sale"],
    "data": [
        # security
        "security/security.xml",
        "security/ir.model.access.csv",
        # data
        "data/data.xml",
        # views
        "views/gov_views.xml",
        "views/area_views.xml",
        "views/res_company.xml",
        "views/stock_warehouse.xml",
        # "views/template.xml",
        "views/shop_template.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": False,
    "category": "tools",
}
