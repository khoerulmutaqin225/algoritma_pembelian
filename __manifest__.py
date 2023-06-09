# -*- coding: utf-8 -*-
{
    'name': "Custome Pembelian V6",

    'summary': """
        Module Custome Pembelian """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Pembelian",
    'website': "http://barokahperkasagroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web','base','product','uom','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/algoritma_pembelian_view.xml',
        'views/algoritma_pembelian_action.xml',
        'views/algoritma_pembelian_menuitem.xml',
        'views/algoritma_pembelian_sequence.xml',
        'views/algoritma_pembelian_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable' : True,
    'application': True,
    'license': 'OEEL-1'
}
