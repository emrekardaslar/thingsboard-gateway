#     Copyright 2021. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import time
from simplejson import dumps

from thingsboard_gateway.connectors.mqtt.mqtt_uplink_converter import MqttUplinkConverter, log


class CustomMqttUplinkConverter(MqttUplinkConverter):
    def __init__(self, config):
        self.__config = config.get('converter')
        self.dict_result = {}
        self.__log = log
        self.__log.info('Custom MQTT uplink converter created')

    def convert(self, topic, body):
        try:
            self.__log.info('Converting uplink message: %s', body)
            self.__log.info('Type of body: %s', type(body))
            #self.dict_result["deviceName"] = topic.split("/")[-1]  # getting all data after last '/' symbol in this case: if topic = 'devices/temperature/sensor1' device name will be 'sensor1'.
            self.dict_result["deviceName"] = "testDevice"
            self.dict_result["deviceType"] = "Thermostat"  # just hardcode this
            self.dict_result["telemetry"] = []  # template for telemetry array
            if type(body) is dict:
                key = list(body.keys())[0]
                if key == 'dev.sta':
                    key = 'status'
                    body[key] = body.pop('dev.sta')
            
                self.dict_result["telemetry"].append(body) 
            else:
                res = {"test": body}  # adding temp value to body            
                #self.dict_result["telemetry"] = {"data": int(body, 0)}
                self.dict_result["telemetry"].append(res)
            return self.dict_result

        except Exception as e:
            log.exception('Error in converter, for config: \n%s\n and message: \n%s\n', dumps(self.__config), body)
            log.exception(e)
