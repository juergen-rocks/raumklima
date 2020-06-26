from sys import stderr

import paho.mqtt.client as mqtt

from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

from rs500common.configuration import ConfigProvider


def on_connect(client, userdata, flags, rc, properties=None):
    if rc != 0:
        print("MQTT connection error: {}".format(mqtt.error_string(rc)), file=stderr)
        raise MQTTError


def save_data_to_mqtt(data: dict, config_file: str) -> None:
    conf = ConfigProvider(config_file).get_config()
    host = conf.get(section="mqtt", option="host", fallback="localhost")
    port = conf.getint(section="mqtt", option="port", fallback=1883)
    client_id = conf.get(section="mqtt", option="clientid", fallback="rs5002mqtt")
    topic_prefix = conf.get(section="mqtt", option="topic_prefix", fallback="rs500")
    topic_suffix = conf.get(section="mqtt", option="topic_suffix", fallback="")
    topic_string = conf.get(section="mqtt", option="topic_string", fallback="{0}/{1}/{2}{3}")

    msg_expiry = conf.get(section="mqtt", option="expiry_time", fallback="false")

    qos = conf.getint(section="mqtt", option="qos", fallback=1)
    retain_s = conf.get(section="mqtt", option="retain", fallback="false")

    username = conf.get(section="mqtt", option="username", fallback=None)
    password = conf.get(section="mqtt", option="password", fallback=None)

    retain = False
    if retain_s.lower() == "true" or retain_s == "1":
        retain = True

    client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)
    client.on_connect = on_connect

    if username is not None and password is not None:
        client.username_pw_set(username, password)

    client.connect(host, port)

    published_messages = []

    if msg_expiry.lower() != "false":
        msg_property = Properties(PacketTypes.PUBLISH)
        try:
            msg_property.MessageExpiryInterval = int(msg_expiry)
        except ValueError as ex:
            raise ValueError("Configuration Error for 'expiry_time'", ex)
    else:
        msg_property = None

    client.loop_start()
    for k, v in data.items():
        (channel, val_typ) = k.split("_")
        topic = topic_string.format(topic_prefix, channel, val_typ, topic_suffix)
        msg_info = client.publish(topic=topic, payload=str(v), retain=retain, qos=qos, properties=msg_property)
        published_messages.append(msg_info)

    for published_message in published_messages:
        published_message.wait_for_publish()
        if published_message.rc != 0:
            print("Publish RC: {}".format(mqtt.error_string(published_message.rc)), file=stderr)

    client.loop_stop()
    client.disconnect()
