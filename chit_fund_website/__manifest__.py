# -*- coding: utf-8 -*-
{
    'name': 'Chit_website',
    'version': '16.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'Doctor Website',
    'depends': ['the_chit_fund', 'portal', 'website', ],
    'data': [
        'views/home.xml',
        'views/myaccount.xml',
        'views/upcoming_chits.xml',
        'views/active_chits.xml',
        'views/history_chits.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            '/chit_fund_website/static/src/js/view_model.js',
            '/chit_fund_website/static/src/js/enquiry.js',
            '/chit_fund_website/static/src/css/home.css',
        ],
    },
    'license': 'LGPL-3',
}
