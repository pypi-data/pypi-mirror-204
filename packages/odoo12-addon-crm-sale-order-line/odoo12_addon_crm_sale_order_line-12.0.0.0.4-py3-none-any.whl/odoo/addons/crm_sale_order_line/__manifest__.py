# -*- coding: utf-8 -*-
{
    'name': "crm_sale_order_line",

    'summary': """
        Add relationship between crm lead and sale order line""",

    'author': "Coopdevs Treball SCCL",
    'website': "",

    'category': 'cooperator',
    'version': '12.0.0.0.4',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'crm',
        'sale',
        'sale_crm'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead.xml'
    ],
    # only loaded in demonstration mode
}
