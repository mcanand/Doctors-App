# -*- coding: utf-8 -*-
{
    'name': 'The chit fund',
    'version': '16.0.0.2',
    'author': 'ANAND MC',
    'summary': 'Chit Fund Management',
    'description': """Manage Chit funds""",
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/update_winner.xml',
        'wizards/pay_due.xml',
        'wizards/daily_pay.xml',
        'views/rules_groups.xml',
        'views/chit_fund.xml',
        'views/chit_month.xml',
        'views/chit_month_partner.xml',
        'views/chit_partner.xml',
        'views/chit_month_bid.xml',
        'views/chit_partner_month_due.xml',
        'views/res_partner.xml',
        'views/res_company.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/the_chit_fund/static/src/css/view_edit.css',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
