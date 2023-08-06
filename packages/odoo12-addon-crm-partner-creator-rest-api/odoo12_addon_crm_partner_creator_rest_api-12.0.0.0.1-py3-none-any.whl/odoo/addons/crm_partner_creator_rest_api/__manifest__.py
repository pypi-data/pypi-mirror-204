# -*- coding: utf-8 -*-
{
    'name': "crm_partner_creator_rest_api",

    'summary': """
        Expose crm partner_creator config on API""",

    'description': """
        Expose crm partner_creator config on API""",

    'author': "Coopdevs Treball SCCL",
    'website': "https://git.coopdevs.org/coopdevs/odoo/odoo-addons/enhancements/enhancements-crm",

    'category': 'crm',
    'version': '12.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'crm_rest_api',
        'crm_partner_creator'
    ],

    # always loaded
    'data': [
    ]
}
