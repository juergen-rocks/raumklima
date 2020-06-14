from sys import stderr

import paho.mqtt.client as mqtt

from rs500common.configuration import ConfigProvider

import time

def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print("MQTT connection error: " + mqtt.error_string(rc), file=stderr)
        raise MQTTError


def save_data_to_mqtt(data: dict, config_file:str) -> None:
    conf = ConfigProvider(config_file).get_config()
    host = conf.get(section="mqtt", option="host", fallback="localhost")
    port = conf.getint(section="mqtt", option="port", fallback=1883)
    clientid = conf.get(section="mqtt", option="clientid", fallback="rs5002mqtt" )
    clean_session_s = conf.get(section="mqtt", option="clean_session", fallback="True")
    topic_prefix =  conf.get(section="mqtt", option="topic_prefix", fallback="rs500")
    topic_suffix =  conf.get(section="mqtt", option="topic_suffix", fallback="")
    topic_string =  conf.get(section="mqtt", option="topic_string", fallback="{0}/{1}/{2}{3}")

    qos = conf.getint(section="mqtt", option="qos" , fallback=1 )
    retain_s = conf.get(section="mqtt", option="retain" , fallback="False")

    username = conf.get(section="mqtt", option="username", fallback=False )
    password = conf.get(section="mqtt", option="password", fallback=False )


    retain = False
    if retain_s == "True":
        retain=True
    clean_session = True
    if clean_session_s == "False":
        clean_session=False

    client = mqtt.Client(client_id = clientid ,clean_session=clean_session)
    client.on_connect=on_connect

    if username is not False and password is not False:
        client.username_pw_set( username , password )

    client.connect( host, port )


    client.loop_start()
    for k,v in data.items():
       ( channel, val_typ ) = k.split("_")
       topic = topic_string.format(topic_prefix, channel, val_typ, topic_suffix )
       msgInfo = client.publish( topic = topic , payload = str(v) , retain=retain , qos = qos)
       msgInfo.wait_for_publish()
       if msgInfo.rc !=  0:
           print ("Publish RC: " + mqtt.error_string(msgInfo.rc))

    client.loop_stop()
    client.disconnect()





