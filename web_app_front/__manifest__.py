# -*- coding: utf-8 -*-
{
    'name': 'Web App Front',
    'version': '16.0.0.1',
    'author': 'ANAND',
    'summary': 'Doctor Website',
    'depends': ['doctors_app', 'base', 'web', 'website', 'portal'],
    'data': [
        'views/layout.xml',
        'views/Home.xml',
        'views/login.xml',
        'views/signup.xml',
        'views/departments.xml',
        'views/loading_page.xml',
        'views/my_account.xml',
        'views/all_doctors.xml',
        'views/today_appointment.xml',
        'views/prescription_list.xml',
        'views/prescription.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            '/web_app_front/static/src/**/*',
            "https://fonts.googleapis.com",
            "https://fonts.gstatic.com",
            "https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap",
        ],
    },
    'license': 'LGPL-3',
}
