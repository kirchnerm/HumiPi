#!/usr/bin/python
import os
import thingspeak
import time
import Adafruit_DHT

import couchdb
import datetime
import json

# CouchDB configuration
couch = couchdb.Server()
#db = couch.create('humidor')
db = couch[os.getenv('HUMIDOR_COUCHDB_NAME', 'humidor')]

# ThingSpeak configuration
channel_id = os.getenv('HUMIDOR_THINGSPEAK_CHANNEL_ID', 0)
write_key  = os.getenv('HUMIDOR_THINGSPEAK_WRITEKEY', '')
read_key   = os.getenv('HUMIDOR_THINGSPEAK_READKEY', '')

# Sensor configuration
pin = os.getenv('HUMIDOR_DHT22_PIN', 22) 
sensor = Adafruit_DHT.DHT22

def putOnCouch(temperature, humidity):
    try:
        timeString = json.dumps(datetime.datetime.now().isoformat())
        doc = { 'datetime': timeString,
                't': temperature, 
                'h': humidity
               }
        
        db.save(doc) 
        
    except:
        print("CouchDB error")
 
def putOnThingspeak(channel, temperature, humidity):
    try:
        response = channel.update({'field1': temperature, 'field2': humidity})
        print('Thinspeak response: ', response )
    except:
        print("connection failed")
            
            
def measure():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        return humidity, temperature
 
    except:
        print("Error reading sensor")
 
 
if __name__ == "__main__":
    channel = thingspeak.Channel(id=channel_id, write_key=write_key, api_key=read_key)

    humidity, temperature = measure()
    print('temperature: {:2.2f}   humidity: {:2.2f} %'.format(temperature, humidity)); 

    putOnCouch(temperature,humidity)
    putOnThingspeak(channel,temperature,humidity)
