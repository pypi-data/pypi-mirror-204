# -*- coding: utf-8 -*-
{
    'name': "easy_my_coop_rest_api",

    'summary': """
    Subscription request service overwritten""",

    'author': "Coopdevs Treball SCCL",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'cooperator',
    'version': '12.0.0.1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'easy_my_coop',
        'easy_my_coop_es',
        'base_rest_base_structure'
    ],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [],
}
