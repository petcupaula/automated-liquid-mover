import os
import sys
from time import sleep
from Adafruit_IO import MQTTClient
from prepare_drinks import Bartender

aio_key = os.environ['AIOKEY']
aio_user = os.environ['AIOUSER']
aio_mqtt = MQTTClient(aio_user, aio_key)
mqtt_feed_sub = 'drink'

def connected(client):
    print('Connected to AIO!  Listening for '+mqtt_feed_sub+' changes...')
    client.subscribe(mqtt_feed_sub)

def disconnected(client):
    print('Disconnected from AIO!')
    # mqtt_run()

def message(client, feed_id, payload):
    print('Feed {feed} received new value: {message}'.format(feed=mqtt_feed_sub, message=payload))
    if payload.lower() == 'fruit mix' or payload.lower() == 'a fruit mix':
        print("Fruit Mix!")
        bartender = Bartender()
        bartender.makeDrink('Fruit Mix')

def setup_mqtt():
    aio_mqtt.on_connect = connected
    aio_mqtt.on_disconnect = disconnected
    aio_mqtt.on_message = message

def mqtt_run():
    aio_mqtt.connect()
    for i in range(20):
        try:
            print('Will try to loop blocking')
            aio_mqtt.loop_blocking()
            print('Loop blocking')
            break
        except:
            print('Error:', sys.exc_info()[0])
            print('Failed loop, waiting 5s...')
            sleep(5)
            continue

if __name__ == '__main__':
    setup_mqtt()
    mqtt_run()
