# -*- coding: utf-8 -*-

from odoo import models, fields


class SMSRecipient(models.TransientModel):
    _inherit = 'sms.resend.recipient'

    oe_reason_code = fields.Selection(
        string='reason code',
        related='notification_id.sms_id.oe_reason_code'
    )

    oe_status_error = fields.Text(
        string='status error',
        related='notification_id.sms_id.oe_status_error'
    )
