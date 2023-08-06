# -*- coding: utf-8 -*-
{
    'name': "product_contract_date_end_unrequired",

    'summary': """
        Avoid date_end to be required on SO line creation from a contract product""",

    'author': "Coopdevs Treball SCCL",
    'website': "",

    'category': 'product_contract',
    'version': '12.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'product_contract'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml'
    ],
    # only loaded in demonstration mode
}
