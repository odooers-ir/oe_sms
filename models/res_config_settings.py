# -- coding: utf-8 --
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sms_provider_type = fields.Selection(
        selection=[
            ('ghasedak', 'Ghasedak'),
            ('kavenegar', 'Kavenegar'),
            ('melipayamak', 'MeliPayamak'),
            ('ippanel', 'IPPanel'),
            ('asanak', 'Asanak'),
            ('odoo_iap', 'Odoo IAP'),
        ],
        string='SMS Provider',
        default='odoo_iap',
        config_parameter='oe_sms.sms_provider_type'
    )

    sms_api_key = fields.Char(
        string='SMS API Key',
        config_parameter='oe_sms.sms_api_key'
    )



    sms_user = fields.Char(
        string='SMS user',
        config_parameter='oe_sms.sms_user'
    )

    sms_password = fields.Char(
        string='SMS password',
        config_parameter='oe_sms.sms_password'
    )


    sms_originator = fields.Char(
        string='SMS originator',
        config_parameter='oe_sms.sms_originator'
    )
