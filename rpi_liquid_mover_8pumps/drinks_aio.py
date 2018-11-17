import os
import sys
import time
import json
import logging
from time import sleep
import RPi.GPIO as GPIO
from Adafruit_IO import MQTTClient
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import AIOconfig

# Assuming for now that the flow rate is the same for all pumps and liquids
FLOW_RATE = 60.0/100.0
# Number of seconds dedicated to cleaning each pump
CLEAN_TIME = 20
# Adafruit IO setup
aio_key = AIOconfig.AIOKEY
aio_user = AIOconfig.AIOUSER
aio_mqtt = MQTTClient(aio_user, aio_key)
mqtt_feed_sub = 'drink'
# Working directory
wd = '/home/paula/automated-liquid-mover/rpi_liquid_mover_8pumps/'
# Logging
LOG_LEVEL = logging.INFO
LOG_FILE = wd + "bartender.log"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

db = None
pumps = {}
inventory = {}

def setup_firebase():
    global db
    cred = credentials.Certificate(wd+'serviceaccount.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

def get_pumps():
    # Read latest mapping of ingredients and pumps
    global pumps
    pumps_ref = db.collection(u'pumps')
    docs = pumps_ref.get()
    for doc in docs:
        pumps[doc.id] = doc.to_dict()
    # Make a dict of available ingredients and the corresponding pin
    global inventory
    for p in pumps.values():
        if p['value']: 
            inventory[p['value']] = p['pin']

def get_recipe(drink):
    #print("Getting recipe for your drink")
    logging.info("Getting recipe for drink")
    drinks_ref = db.collection(u'drinks')
    doc = drinks_ref.document(drink).get()
    drink_doc = doc.to_dict()
    if drink_doc is None:
        print("Getting drink by name")
        docs = drinks_ref.where(u'available', u'==', True).get()
        print(docs)
        for doc in docs:
            if doc.to_dict()['name'].lower() == drink.lower() or ("a" + doc.to_dict()['name'].lower()) == drink.lower():
               drink_doc = doc.to_dict()
    print(drink_doc)
    logging.info(drink_doc['name'])
    recipe = drink_doc['ingredients']
    print(recipe)
    logging.info(recipe)
    return recipe
        

def connected(client):
    print('Connected to AIO!  Listening for '+mqtt_feed_sub+' changes...')
    client.subscribe(mqtt_feed_sub)

def disconnected(client):
    print('Disconnected from AIO!')
    # mqtt_run()

def message(client, feed_id, payload):
    print('Feed {feed} received new value: {message}'.format(feed=mqtt_feed_sub, message=payload))
    make_drink(payload)

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

def setup_pins():
    GPIO.setmode(GPIO.BCM)
    # Loop through pins and set mode and state to 'low'
    for pump in pumps.keys():
        print("Configuring pin", str(pumps[pump]["pin"]))
        GPIO.setup(pumps[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH)
    
def pour(pin, pourTime):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(pourTime)
    GPIO.output(pin, GPIO.HIGH)

def make_drink(drink):
    logging.info("Received a drink order")

    if drink == "clean":
        clean()
        return

    get_pumps()
    recipe = get_recipe(drink)

    logging.info("Drink preparation started: "+drink)
    for step in recipe.keys():
        pin = inventory[step]
        ml = recipe[step]
        pourTime = ml * FLOW_RATE
        print("Pouring for", pourTime)
        pour(pin, pourTime)
    #print("Finished preparing drink. Enjoy!")
    logging.info("Drink preparation finished")

def clean():
    #print("Starting to clean pumps one by one")
    logging.info("Cleaning started")
    for pump in pumps.keys():
        print("Cleaning", pump)
        pour(pumps[pump]["pin"], CLEAN_TIME)
    logging.info("Cleaning finished")

if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
    setup_firebase()
    get_pumps()
    setup_pins()
    setup_mqtt()
    mqtt_run()
