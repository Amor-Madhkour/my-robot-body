
from enum import Enum

# the APP assigns a specific ESP VALUE based on KEY.
# these constants are needed to know immediately if the KEY is related to an ESP VALUE belonging to a MULTI-VALUE esp
# or a SINGLE-VALUE esp.


# this ENUM contains the types of ESP CHANNLE, so we can assign to each esp-value-type also the channel type
class ESP_CHANNEL_TYPE(Enum):
    SINGLE_VALUE=0
    MULTI_VALUE=1
    AGGREGATIONE_VALUE=2
    PASS_THROGHT=3


class ESP_VALUE_TYPE_KEYS(Enum):
    ANGLE_X = 'ax'
    ANGLE_Y = 'ay'
    ANGLE_Z = 'az'
    GYRO_X = 'gx'
    GYRO_Y = 'gy'
    GYRO_Z = 'gz'
    MICROPHONE = 'm'
    SONAR = 's'


class EspValueType:
    def __init__(self, key, channel_type, min_in, max_in):

        self.key = key
        self.channel_type = channel_type

        # the value coming from ESP is in this value range
        self.min_in = min_in
        self.max_in = max_in


# this ENUM contains all the possible ESP VALUES configs.
# it's important that the VALUES are UNIQUE.
esp_value_types = {

    # --- ACCELEROMETER
    ESP_VALUE_TYPE_KEYS.ANGLE_X.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.ANGLE_X.value, ESP_CHANNEL_TYPE.MULTI_VALUE, -3, 3),
    ESP_VALUE_TYPE_KEYS.ANGLE_Y.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.ANGLE_Y.value, ESP_CHANNEL_TYPE.MULTI_VALUE, -3, 3),
    ESP_VALUE_TYPE_KEYS.ANGLE_Z.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.ANGLE_Z.value, ESP_CHANNEL_TYPE.MULTI_VALUE, -3, 3),
    ESP_VALUE_TYPE_KEYS.GYRO_X.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.GYRO_X.value, ESP_CHANNEL_TYPE.MULTI_VALUE, -3, 3),
    ESP_VALUE_TYPE_KEYS.GYRO_Y.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.GYRO_Y.value, ESP_CHANNEL_TYPE.MULTI_VALUE, -3, 3),
    ESP_VALUE_TYPE_KEYS.GYRO_Z.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.GYRO_Z.value, ESP_CHANNEL_TYPE.MULTI_VALUE, -3, 3),

    # --- MICROPHONE
    ESP_VALUE_TYPE_KEYS.MICROPHONE.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.MICROPHONE.value, ESP_CHANNEL_TYPE.SINGLE_VALUE, 0, 10),
        

    # --- SONAR
    ESP_VALUE_TYPE_KEYS.SONAR.value:
        EspValueType(ESP_VALUE_TYPE_KEYS.SONAR.value, ESP_CHANNEL_TYPE.SINGLE_VALUE, 10, 200)
}