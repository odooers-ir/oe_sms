# -*- coding: utf-8 -*-


import logging
from odoo import models, fields, tools, _

from werkzeug.urls import url_join
from .sms_api import SmsApi

_logger = logging.getLogger(__name__)


class SmsSms(models.Model):
    _inherit = 'sms.sms'

    oe_reason_code = fields.Selection(
        selection=[
            ('0', 'No error'),
            ('20', 'Recipient number unreachable'),
            ('21', 'Recipient number incorrect'),
            ('22', 'Delivery Failure'),
            ('31', 'The recipient is blacklisted (e.g. People that respond "STOP" to an earlier message can appear '
                   'in the blacklist)')
        ],
        string='reason code',
        copy=False,
    )
    oe_status_code = fields.Integer(
        string='status code',
        default=200,
        copy=False,
    )
    oe_status_error = fields.Text(
        string='status error',
        copy=False,
    )
    sms_send_from = fields.Selection(
        selection=[
            ('ghasedak', 'Ghasedak'),
            ('kavenegar', 'Kavenegar'),
            ('melipayamak', 'MeliPayamak'),
            ('ippanel', 'IPPanel'),
            ('asanak', 'Asanak'),
            ('odoo_iap', 'Odoo IAP')],
        string='SMS send from',
        copy=False,
    )
   
 
   
   
    def _send(self, unlink_failed=False, unlink_sent=True, raise_exception=False):
        """Send SMS after checking the number (presence and formatting)."""

        print("ttttttttttttttttttDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDd")

        messages = [{
            'content': body,
            'numbers': [{'number': sms.number, 'uuid': sms.uuid} for sms in body_sms_records],
        } for body, body_sms_records in self.grouped('body').items()]

        delivery_reports_url = url_join(self[0].get_base_url(), '/sms/status')
        try:
            results = SmsApi(self.env)._send_sms_batch(messages, delivery_reports_url=delivery_reports_url)
        except Exception as e:
            _logger.info('Sent batch %s SMS: %s: failed with exception %s', len(self.ids), self.ids, e)
            if raise_exception:
                raise
            
            sms_provider_type = self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_provider_type')
            kave=False
            meli=False
            ghased=False
            ipp=False
            asa=False

            if sms_provider_type == 'melipayamak':
                meli=True
            
            if sms_provider_type == 'kavenegar':
                kave=True
            
            if sms_provider_type == 'ghasedak':
                ghased=True

            if sms_provider_type == 'ippanel':
                ipp=True

            if sms_provider_type == 'asanak':
                asa=True

            results = [{'uuid': sms.uuid, 'state': 'server_error', 'kavenegar': kave,'melipayamak': meli,'ghasedak': ghased,'ippanel': ipp,'asanak' :asa} for sms in self]

        else:
            _logger.info('Send batch %s SMS: %s: gave %s', len(self.ids), self.ids, results)

        results_uuids = [result['uuid'] for result in results]
        all_sms_sudo = self.env['sms.sms'].sudo().search([('uuid', 'in', results_uuids)]).with_context(sms_skip_msg_notification=True)
       
        print ("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        print(results)
        print (results_uuids)
        print (all_sms_sudo)
        
        for iap_state, results_group in tools.groupby(results, key=lambda result: result['state']):
            sms_sudo = all_sms_sudo.filtered(lambda s: s.uuid in {result['uuid'] for result in results_group})
            
            ###################################################################
            for ss in sms_sudo:
                ###############
                print("KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
                results_kave = [result['uuid'] for result in results if result['kavenegar']] 
                print (results_kave)
                if ss.uuid in results_kave:
                    print ("ssssssssssssssssssss")
                    print (ss)
                    ss.write({'sms_send_from': 'kavenegar'})
                ##############

                ###############
                print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                results_meli = [result['uuid'] for result in results if result['melipayamak']] 
                print (results_meli)
                if ss.uuid in results_meli:
                    print ("iiiiiiiiiiiiiiiii")
                    print (ss)
                    ss.write({'sms_send_from': 'melipayamak'})
                ##############

                ###############
                print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                results_ghased = [result['uuid'] for result in results if result['ghasedak']] 
                print (results_ghased)
                if ss.uuid in results_ghased:
                    print ("iiiiiiiiiiiiiiiii")
                    print (ss)
                    ss.write({'sms_send_from': 'ghasedak'})
                ##############
            
             ###############
                print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                results_ipp = [result['uuid'] for result in results if result['ippanel']] 
                print (results_ipp)
                if ss.uuid in results_ipp:
                    print ("iiiiiiiiiiiiiiiii")
                    print (ss)
                    ss.write({'sms_send_from': 'ippanel'})
                ##############

            ###############
                print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
                results_asa = [result['uuid'] for result in results if result['asanak']] 
                print (results_asa)
                if ss.uuid in results_asa:
                    print ("iiiiiiiiiiiiiiiii")
                    print (ss)
                    ss.write({'sms_send_from': 'asanak'})
                ##############
            #############################################################
            if success_state := self.IAP_TO_SMS_STATE_SUCCESS.get(iap_state):
                sms_sudo.sms_tracker_id._action_update_from_sms_state(success_state)
                to_delete = {'to_delete': True} if unlink_sent else {}
                sms_sudo.write({'state': success_state, 'failure_type': False, **to_delete})
            else:
                failure_type = self.IAP_TO_SMS_FAILURE_TYPE.get(iap_state, 'unknown')
                if failure_type != 'unknown':
                    sms_sudo.sms_tracker_id._action_update_from_sms_state('error', failure_type=failure_type)
                else:
                    sms_sudo.sms_tracker_id._action_update_from_provider_error(iap_state)
                to_delete = {'to_delete': True} if unlink_failed else {}
                sms_sudo.write({'state': 'error', 'failure_type': failure_type, **to_delete})

        all_sms_sudo.mail_message_id._notify_message_notification_update()

  


    def action_generate_activity(self, error_message, res_model_id, res_id, sms_id):
        context = dict(self._context) or {}
        if res_model_id and res_id:
            record_id = self.env[res_model_id].browse(res_id)
            if not context.get('from_sms_api'):
                error_message = "Message sent failed due to '%s'" % dict(
                    sms_id._fields['oe_reason_code']._description_selection(sms_id.env)).get(error_message)
            if isinstance(record_id, type(self.env['mail.activity.mixin'])):
                record_id.with_context(active_model=res_model_id, active_id=res_id).activity_schedule(
                    summary='SMS Sent Failed',
                    activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
                    user_id=self.env.user.id,
                    note=error_message
            )
