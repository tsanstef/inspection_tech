# -*- coding: utf-8 -*-
{
    'name': "Inspections of Technical Equipment",

    'summary': """
        Manages the process of inspection of technical equipment""",

    'description': """
        Supports service providers who specialize in technical inspections of
        technical equipment such as cranes, hoists, etc
    """,

    'author': "RootRock",
    'website': "http://www.rootrock.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Service',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/inspection_tech.xml',
        'views/partner.xml',
        'views/equipment_type_view.xml',
        'views/inspection_tech_types.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}