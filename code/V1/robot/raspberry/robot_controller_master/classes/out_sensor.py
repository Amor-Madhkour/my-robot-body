
from typing import Self
from utils.util_methods import parse_serial_message
from configs.esps.esp_types import ESP_CHANNEL_TYPE
import numpy as np





# class used to handle the relay of messages from hardware from serial
class outSensor:

    def __init__(self, ID):

        #self.serial_value = serial_value
        self.channel_type = None
        self.serial = ID

    def on_esp_msg_rcv(self, string_msg):
        pass
    


class PassThroughChannel(outSensor):

    def __init__(self, ID, in_sensor_value):
        super(PassThroughChannel, self).__init__(ID)

        # the channel contains a single esp value.
        self.esp_value = in_sensor_value

        self.channel_type = ESP_CHANNEL_TYPE.PASS_THROGHT

    def on_esp_msg_rcv(self, string_msg):
        # called when a UDP msg is received from ESP.
        # esp UDP messages for 'single-value' are in the form 'value'

        # 1. transmit message to the esp_value
        # print(f"[SingleValueEspChannel][on_esp_msg_rcv] - ip: {self.ip} - message: '{string_msg}'")

        self.esp_value.on_msg_received(string_msg)


class AggregateChannel(outSensor):

    def __init__(self, ID):
        super(AggregateChannel, self).__init__(ID)

        # the channel contains a number of "esp values" that are the values
        # that come from the ESP and need to be sent to Arduino after a processing
        # it's an esp_value_key:esp_value dict.
        self.insensor_values = dict()
        self.aggregation_function = None
        #current values that have to be aggregated
        self.aggregation_value = []
        #aggregated values
        self.aggregate_values= 0

        self.channel_type = ESP_CHANNEL_TYPE.AGGREGATIONE_VALUE

    def add_esp_value(self, insensor_value):
        # this overrides any ESP_VALUE with the same key
        self.insensor_values[insensor_value.serial_value_type.key] = insensor_value

    def remove_esp_value(self, insensor_value_key):
        del self.insensor_values[insensor_value_key]

    def on_esp_msg_rcv(self, string_msg):
        # called when a UDP msg is received from ESP.
        # esp UDP messages for 'multi-value' are in the form 'key:val:_key_val_..'

        # 1. get individual messages
        # 2. for each individual key-value msg,
        #    call the "on_msg_rcv" of the EspValue with the corresponding KEY

        all_key_val_msgs = string_msg
        # print(f"[MultiValueEspChannel][on_esp_msg_rcv] - ip: {self.ip} - messages: '{all_key_val_msgs}'")
        self.update_values(all_key_val_msgs)
        for msg in all_key_val_msgs:
            self.insensor_values[msg.key].on_msg_received(msg.value)
     
    def aggregate_values(self):
        
        if self.aggregation_function is not None:
            if len(self.insensor_values) == 0:
              raise ValueError("the dict is empty")
            self.aggregate_values = self.get_aggregation_value()
            
            

    def update_values(self, all_key_val_msgs):
        for temp in all_key_val_msgs.values():
            self.aggregation_value.append(temp.value)

    def set_aggregation_function(self, aggregation_function):
        self.aggregation_function = aggregation_function

    def get_aggregation_value(self):
        return self.aggregate_values

   
                    
        