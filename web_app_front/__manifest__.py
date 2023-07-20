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
        'views/login.xml',
        'views/signup.xml',
        'views/loading_page.xml',
        'views/Doctor_account_view.xml',
        'views/Patient_account_view.xml',

    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            '/web_app_front/static/src/css/layout.css',
            '/web_app_front/static/src/css/login.css',
            '/web_app_front/static/src/css/signup.css',
            '/web_app_front/static/src/css/doctor_account_view.css',

        ],
    },
    'license': 'LGPL-3',
}
