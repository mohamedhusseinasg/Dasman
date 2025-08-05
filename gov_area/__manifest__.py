{
    'name': 'Web Dasman Project',
    'version': '1.0',
    'summary': 'Interactive whiteboard with GOV and ARFAS management',
    'description': 'Module for managing government and areas data with whiteboard functionality',
    'author': 'Your Company',
    'website': 'https://www.yourwebsite.com',
    'category': 'Tools',
    'depends': ['base', 'web','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/gov_views.xml',
        'views/area_views.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'web_whiteboard/static/src/js/whiteboard.js',
    #     ],
    # },
    'installable': True,
    'application': True,
}