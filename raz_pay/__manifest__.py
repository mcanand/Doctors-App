{
    'name': 'Razor Pay payment acquirer',
    'version': '15.0.1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 1,
    'summary': "Razor Pay payment aquirer",
    'depends': ['payment'],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_acquirer.xml',
        'views/payment_acquirer.xml',
        'views/payment_details.xml',
    ],
    'application': False,
    'assets': {
        'web.assets_frontend': [

        ],
    },
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
