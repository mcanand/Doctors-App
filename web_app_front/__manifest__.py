# -*- coding: utf-8 -*-
{
    'name': 'Web App Front',
    'version': '16.0.0.1',
    'author': 'ANAND',
    'summary': 'Doctor Website',
    'depends': ['doctors_app', 'base', 'web', 'website'],
    'data': [
        'views/layout.xml',
        'views/Home.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            '/web_app_front/static/src/css/layout.css',
        ],
    },
    'license': 'LGPL-3',
}
