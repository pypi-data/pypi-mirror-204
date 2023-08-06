# -*- coding: utf-8 -*-
{
    'name': "crm_sale_order_line_contract",

    'summary': """
        Add relationship between crm lead and sale order line for contract products""",

    'author': "Coopdevs Treball SCCL",
    'website': "",

    'category': 'cooperator',
    'version': '12.0.0.0.3',

    # any module necessary for this one to work correctly
    'depends': [
        'crm_sale_order_line',
        'product_contract'
    ],

    # always loaded
    'data': [
        'views/crm_lead.xml',
        'views/sale_order.xml'
    ],
    # only loaded in demonstration mode
}
