# -*- coding: utf-8 -*-
{
    'name': "Multiple SMS Gateway",

    'summary': """
        Send SMS via Iranian Provider...
    """,

    'description': """
        Send SMS via Iranian Provider...
    """,

    'author': "odooers.ir",
    'website': "https://www.odooers.ir",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '18.0.1.0.1',
    'depends': ['sms'],

    # always loaded
    'data': [
        'wizard/sms_resend_view.xml',
        'views/sms_sms_view.xml',
        'views/res_config_settings_views.xml',
    ]
}

