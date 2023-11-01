{
    'name': 'Documents Attachments',
    'version': '1.0',
    'author': 'Anand',
    'category': 'Custom',
    'summary': 'documents attach to contacts',
    'depends': ['base',],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/document_attach.xml',




    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
