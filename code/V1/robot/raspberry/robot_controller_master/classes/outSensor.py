from utils.util_methods import parse_serial_message
from configs.esps.esp_types import ESP_CHANNEL_TYPE
#TODO add the class of the inSensor AND maging the aggregation of the value

# class used to handle the creation of the sending message to the end-device suh as esp or oculus
# save its IP and PORT, and respond
class outSensor:
##onGoingVal is the corrisponding class of esp_value

    def __init__(self,sensor_Dof,onGoingVal):

        self.channel_type = None
        #ip and Key of the message
        self.sensor_Dof= sensor_Dof
        #class that contains current,last and tolerance and
        self.onGoingVal = onGoingVal

    def on_esp_msg_rcv(self, string_msg):
        pass


class PassThroughChannel(outSensor):

    def __init__(self, sensor_Dof,onGoingVal):
        super(PassThroughChannel, self).__init__(sensor_Dof,onGoingVal)

        # the channel contains a single esp value.
        self.channel_type = ESP_CHANNEL_TYPE.PASS_THROGHT

    def on_esp_msg_rcv(self, string_msg):
        # called when a UDP msg is received from ESP.
        # esp UDP messages for 'single-value' are in the form 'value'

        # 1. transmit message to the esp_value
        # print(f"[PassThroughChannel][on_esp_msg_rcv] - ip: {self.ip} - message: '{string_msg}'")

        self.esp_value.on_msg_received(string_msg)


class AggregateChannel(outSensor):

    def __init__(self,sensor_Dof,onGoingVal):
        super(AggregateChannel, self).__init__(sensor_Dof,onGoingVal)

        # the channel contains a number of "esp values" that are the values
        # that come from the ESP and need to be sent to Arduino after a processing
        # it's an esp_value_key:esp_value dict.
        self.inSensor = dict()
        self.channel_type = ESP_CHANNEL_TYPE.AGGREGATIONE_VALUE

    def add_esp_value(self, inSensor_value):
        # this overrides any ESP_VALUE with the same key
        self.esp_values[inSensor_value.inSensor_value_type.key] = inSensor_value

   
    #create a list of the sensor that are in the aggregation
    def add_inSensor(self, inSensor):
        # this overrides any ESP_VALUE with the same key
        self.inSensor[inSensor.sensor_Dof] = inSensor

    

    def aggregate(self, string_msg):
        pass
  
    def updateSensor(self):
        # called when a UDP msg is received from ESP.
        # esp UDP messages for 'multi-value' are in the form 'key:val:_key_val_..'
        temp= aggregate("fwsfsf")
        self.onGoingVal.set_current(temp)
        
        all_key_val_msgs = parse_serial_message(string_msg)

        # print(f"[MultiValueEspChannel][on_esp_msg_rcv] - ip: {self.ip} - messages: '{all_key_val_msgs}'")

        for msg in all_key_val_msgs:
            self.esp_values[msg.key].on_msg_received(msg.value)
