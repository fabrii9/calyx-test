# -*- coding: utf-8 -*-
{
  'name': "Calyx - test",

  'summary': """
        """,

  'description': """
    """,

  'author': "Fabrizio Dominguez",
  'website': "http://misitio.com",

  # Categories can be used to filter modules in modules listing
  # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
  # for the full list
  'category': 'Sales',
  'version': '1.0.1',

  # any module necessary for this one to work correctly
  'depends': ['account', 'sale', 'stock'],

  # always loaded
  'data': [
    'security/ir.model.access.csv',
    'data/sale_channel_data.xml',
    'views/view_sale_channels.xml',
    'views/view_order_form.xml',
    'views/view_move_form.xml',
    'views/view_credit_groups.xml',
    'views/view_res_partner_form.xml'
  ],

}
