# -*- coding: utf-8 -*-
import json
import requests
from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

from odoo.addons.sms.tools.sms_api import SmsApi


class SmsApi(SmsApi):
    
    def _send_sms_melli(self,  message,number,sms_api_key,sms_originator):
        method = "POST"
        headers = {"Content-Type": "application/json"}
        data = {
            "to": number,
            "from": sms_originator,
            "text": message,
        }
        try:
            print ('https://console.melipayamak.com/api/send/simple/'+sms_api_key)
            response = requests.post('https://console.melipayamak.com/api/send/simple/'+sms_api_key, json=data)
            print(response)


           # response = requests.request(method, "https://rest.payamak-panel.com/api/SendSMS/SendSMS", json=data, headers=headers, timeout=60)
            print ("Fffffffffffffffffffffffffff")
            print (response)
            #response.raise_for_status()
        except Exception as e:
            _logger.error('An error encountered: %s ' % e)
        return response

    def _send_sms_kaveh(self, message,number,sms_api_key,sms_originator):
        method = "GET"
    
        try:
            url="https://api.kavenegar.com/v1/"+sms_api_key+"/sms/send.json?receptor="+ number+"&sender="+sms_originator+"&message="+message
            
            print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDd")
            
            print(url)

            response = requests.request(method, url)
            #response.raise_for_status()
            print (response)

        except Exception as e:
            _logger.error('An error encountered: %s ' % e)

        return response.json()
    
    def _send_sms_ghasedak(self,  message,number,sms_api_key,sms_originator):
        
        print ("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
      
        number = number.replace("+98", "0")

        url = "http://api.ghasedaksms.com/v2/sms/send/simple"
        method = "POST"
        headers = {'apikey': sms_api_key}
        data = {
            "Receptor": number,
            "sender": sms_originator,
            "message": message,
        }
        try:
            response = requests.request("POST", url, data=data, headers=headers)
            print(response)


           # response = requests.request(method, "https://rest.payamak-panel.com/api/SendSMS/SendSMS", json=data, headers=headers, timeout=60)
            print ("Fffffffffffffffffffffffffff")
            print (response)
            #response.raise_for_status()
        except Exception as e:
            _logger.error('An error encountered: %s ' % e)
        return response

    def _send_sms_ippanel(self,  message,number,sms_api_key,sms_originator):
        
        print ("ffffffffffffffff")
      
       # number = number.replace("+98", "0")

        url = "https://api2.ippanel.com/api/v1/sms/send/webservice/single"
        method = "POST"
        headers = {'accept':'application/json' , 'apikey': sms_api_key,'Content-Type': 'application/json'}
        data = {
            "Receptor": number,
            "sender": sms_originator,
            "message": message,

            "recipient": [
                number
            ],
            "sender": sms_originator,
            "message": message,
        }
        try:
            response = requests.request("POST", url, data=json.dumps(data), headers=headers)
            #response = requests.request("POST", url, data=data, headers=headers)
            print(response)


           # response = requests.request(method, "https://rest.payamak-panel.com/api/SendSMS/SendSMS", json=data, headers=headers, timeout=60)
            print ("Fffffffffffffffffffffffffff")
            print (response)
            #response.raise_for_status()
        except Exception as e:
            _logger.error('An error encountered: %s ' % e)
        return response

    def _send_sms_asanak(self,  message,number,sms_user,sms_password,sms_originator):
        
        print ("ffffffffffffffff")
      
        number = number.replace("+98", "0")

        url = "https://sms.asanak.ir/webservice/v2rest/sendsms"
        method = "POST"
        #headers = {'accept':'application/json' , 'apikey': sms_api_key,'Content-Type': 'application/json'}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            
            'username': sms_user,
            'password': sms_password,
            'source': sms_originator,
            'message': message,
            'destination':[number],

        }

        print (data)
        try:
            response = requests.request("POST", url, data=data,  headers=headers, timeout=5)
            #response = requests.request("POST", url, data=data, headers=headers)
            print(response)


           # response = requests.request(method, "https://rest.payamak-panel.com/api/SendSMS/SendSMS", json=data, headers=headers, timeout=60)
            print ("Fffffffffffffffffffffffffff")
            print (response)
            #response.raise_for_status()
        except Exception as e:
            _logger.error('An error encountered: %s ' % e)
        return response

    
    
    
    def _send_sms_single(self, message, number):
        sms_provider_type = self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_provider_type')
        sms_api_key =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_api_key')
        sms_originator =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_originator')
        status_code = 0
        if sms_provider_type == 'melipayamak':
            response = self._send_sms_melli(message,number,sms_api_key,sms_originator)
            status_code = response.status_code
        
        if sms_provider_type == 'kavenegar':
            response = self._send_sms_kaveh(message,number,sms_api_key,sms_originator)
            return_value = response['return']
            status_code = return_value['status']
            
        if sms_provider_type == 'ghasedak':
            response = self._send_sms_ghasedak(message,number,sms_api_key,sms_originator)
            status_code = response.status_code

        return status_code
    
    def _send_sms_batch(self, messages, delivery_reports_url=False):
        print ("innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        """
        Override of default Odoo function to send SMS messages
        ODOO URL: https://github.com/odoo/odoo/blob/d04c8b7e484db8306d858c891a7a2b11885fdcd9/addons/sms/models/sms_api.py#L38
        """
        sms_provider_type = self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_provider_type')
        
        print ("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        print (sms_provider_type)

        if sms_provider_type == 'melipayamak':
            return_values = []
            
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #ir_config_param = self.env['ir.config_parameter'].sudo().get_param
            #sms_user = ir_config_param('oe_sms.sms_user')
            #sms_password = ir_config_param('oe_sms.sms_password')
            #sms_originator = ir_config_param('oe_sms.sms_originator')

            sms_api_key =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_api_key')
            sms_originator =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_originator')
            print (messages)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                
            for message in messages:
                
                for number in message['numbers']:
           
                    response = self._send_sms_melli(message['content'],number['number'],sms_api_key,sms_originator)    
                
                    print ("responseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                    print (response)
                    
                    return_value = {
                        'uuid': number.get('uuid'),
                        'state': 'success',
                        'credit': 0,
                        'kavenegar': False,
                        'melipayamak': True,
                        'ghasedak': False,
                        'ippanel': False,
                        'asanak':False
                    }
                    rj=response.json()
                    recid=rj['recId']
                    sts=  rj ['status']
                    if response.status_code != 200:
                        sms_id = self.env['sms.sms'].sudo().browse(number['uuid'])
                        #error_code = json.dumps(json.loads(response.text), indent=4)
                        sms_id.write({
                            'oe_status_code': response.status_code,
                            'oe_status_error': sts,
                        })
                        sms_id.with_context(from_sms_api=True).action_generate_activity(
                            sts, sms_id.mail_message_id.model, sms_id.mail_message_id.res_id, sms_id)
                        return_value.update({ 'state': 'server_error',
                                           'kavenegar': False,
                                           'melipayamak': True,
                                           'ghasedak': False,
                                            'ippanel': False ,
                                            'asanak':False }) 

                    return_values.append(return_value)

            return return_values
        
        if sms_provider_type == 'kavenegar':
            
            print ("uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu")

            return_values = []
            
            #ir_config_param = self.env['ir.config_parameter'].sudo().get_param

            #print (ir_config_param)
          
            sms_api_key =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_api_key')
            sms_originator =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_originator')

            
            for message in messages:
                
                for number in message['numbers']:
           
                    response = self._send_sms_kaveh(message['content'],number['number'],sms_api_key,sms_originator)
                    print(response)
                    return_value = {
                        'uuid': number.get('uuid'),
                        'state': 'success',
                        'credit': 0,
                        'kavenegar': True,
                        'melipayamak': False,
                        'ghasedak': False,
                        'ippanel': False ,
                        'asanak':False
                    }
                    re=response['return']
                    ent=  response['entries'][0]
                    return_code= re['status']
                    status= ent ['status']
                    stm =  ent['statustext']
                                    
                    print (status)
                    print (stm)



                    if return_code != 200:
                        sms_id = self.env['sms.sms'].sudo().browse(number['uuid'])
                        #error_code = json.dumps(json.loads(response.text), indent=4)
                        sms_id.write({
                            'oe_status_code':status ,
                            'oe_status_error': stm,
                        })
                        sms_id.with_context(from_sms_api=True).action_generate_activity(stm, sms_id.mail_message_id.model, sms_id.mail_message_id.res_id, sms_id)
                        return_value.update({ 'state': 'server_error',
                                           'kavenegar': True,
                                           'melipayamak': False,
                                           'ghasedak': False,
                                            'ippanel': False ,
                                            'asanak':False  })
                    
                    return_values.append(return_value)

            return return_values
        

        if sms_provider_type == 'ghasedak':
            return_values = []
            
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #ir_config_param = self.env['ir.config_parameter'].sudo().get_param
            #sms_user = ir_config_param('oe_sms.sms_user')
            #sms_password = ir_config_param('oe_sms.sms_password')
            #sms_originator = ir_config_param('oe_sms.sms_originator')

            sms_api_key =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_api_key')
            sms_originator =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_originator')
            print (messages)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                
            for message in messages:
                
                for number in message['numbers']:
           
                    response = self._send_sms_ghasedak(message['content'],number['number'],sms_api_key,sms_originator)    
                
                    print ("responseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                    print (response)
                    
                    return_value = {
                        'uuid': number.get('uuid'),
                        'state': 'success',
                        'credit': 0,
                        'kavenegar': False,
                        'melipayamak': False,
                        'ghasedak': True,
                        'ippanel': False,
                        'asanak':False
                    }
                    rj=response.json()
                    
                    print(response.text)
                    print(rj)
                  
                    sts=  rj ['result']
                    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                    print (sts)
                    if response.status_code != 200:
                        recid=rj['messageids']
                        sms_id = self.env['sms.sms'].sudo().browse(number['uuid'])
                        #error_code = json.dumps(json.loads(response.text), indent=4)
                        sms_id.write({
                            'oe_status_code': response.status_code,
                            'oe_status_error': recid,
                        })
                        sms_id.with_context(from_sms_api=True).action_generate_activity(
                            sts, sms_id.mail_message_id.model, sms_id.mail_message_id.res_id, sms_id)
                        return_value.update({ 'state': 'server_error',
                                           'kavenegar': False,
                                           'melipayamak': False ,
                                           'ghasedak': True,
                                            'ippanel': False,
                                            'asanak':False }) 

                    return_values.append(return_value)

            return return_values
      

        if sms_provider_type == 'ippanel':
            return_values = []
            
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #ir_config_param = self.env['ir.config_parameter'].sudo().get_param
            #sms_user = ir_config_param('oe_sms.sms_user')
            #sms_password = ir_config_param('oe_sms.sms_password')
            #sms_originator = ir_config_param('oe_sms.sms_originator')

            sms_api_key =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_api_key')
            sms_originator =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_originator')
            print (messages)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                
            for message in messages:
                
                for number in message['numbers']:
           
                    response = self._send_sms_ippanel(message['content'],number['number'],sms_api_key,sms_originator)    
                
                    print ("responseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                    print (response)
                    
                    return_value = {
                        'uuid': number.get('uuid'),
                        'state': 'success',
                        'credit': 0,
                        'kavenegar': False,
                        'melipayamak': False,
                        'ghasedak': False,
                        'ippanel': True,
                        'asanak':False
                    }
                    rj=response.json()
                    
                    print(response.text)
                    print(rj)

                    status= rj ['status']
                    stm =  rj['error_message']
                                    
                    print (status)
                    print (stm)
                  
                   
                    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
              
                    if response.status_code != 200:
                    
                        sms_id = self.env['sms.sms'].sudo().browse(number['uuid'])
                        #error_code = json.dumps(json.loads(response.text), indent=4)
                        sms_id.write({
                            'oe_status_code': status,
                            'oe_status_error': stm,
                        })
                        sms_id.with_context(from_sms_api=True).action_generate_activity(
                            stm, sms_id.mail_message_id.model, sms_id.mail_message_id.res_id, sms_id)
                        return_value.update({ 'state': 'server_error',
                                           'kavenegar': False,
                                           'melipayamak': False ,
                                           'ghasedak': False,
                                           'ippanel': True,
                                            'asanak':False }) 

                    return_values.append(return_value)

            return return_values
      
        if sms_provider_type == 'asanak':
            return_values = []
            
            print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #ir_config_param = self.env['ir.config_parameter'].sudo().get_param
            #sms_user = ir_config_param('oe_sms.sms_user')
            #sms_password = ir_config_param('oe_sms.sms_password')
            #sms_originator = ir_config_param('oe_sms.sms_originator')

            #sms_api_key =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_api_key')
            
            sms_originator =  self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_originator')
            sms_user = self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_user')
            sms_password = self.env['ir.config_parameter'].sudo().get_param('oe_sms.sms_password')


            print (messages)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                
            for message in messages:
                
                for number in message['numbers']:
           
                    response = self._send_sms_asanak(message['content'],number['number'],sms_user,sms_password,sms_originator)    
                
                    print ("responseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                    print (response)
                    
                    return_value = {
                        'uuid': number.get('uuid'),
                        'state': 'success',
                        'credit': 0,
                        'kavenegar': False,
                        'melipayamak': False,
                        'ghasedak': False,
                        'ippanel': False,
                        'asanak':True
                    }
                    rj=response.json()
                    
                    print(response.text)
                    print(rj)
                    asmt= rj['meta']
                    status= asmt ['status']
                    stm =  asmt['message']
                                    
                    print (status)
                    print (stm)
                  
                   
                    print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
              
                    if response.status_code != 200:
                    
                        sms_id = self.env['sms.sms'].sudo().browse(str(number['uuid']))
                        #error_code = json.dumps(json.loads(response.text), indent=4)
                        print (number['uuid'])
                        print (sms_id)
                        sms_id.write({
                            'oe_status_code': status,
                            'oe_status_error': stm,
                        })
                        sms_id.with_context(from_sms_api=True).action_generate_activity(
                            stm, sms_id.mail_message_id.model, sms_id.mail_message_id.res_id, sms_id)
                        return_value.update({ 'state': 'server_error',
                                           'kavenegar': False,
                                           'melipayamak': False ,
                                           'ghasedak': False,
                                           'ippanel': False,
                                            'asanak':True }) 

                    return_values.append(return_value)

            return return_values
      
       
       
        return super(SmsApi, self)._send_sms_batch(messages, delivery_reports_url)
