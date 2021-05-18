# Created by Rui Santos
# Complete project details: https://randomnerdtutorials.com
#
# SQLite version 3.8.6 2014-08-15 11:46:33

import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import eventlet
from datetime import datetime    # show date
import time                      # time
import csv        # for storing data
import psycopg2 as psql   # PostgreSQL
import json
import atexit

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xDsTbiULqIrqXkO_X5kcyg'
socketio = SocketIO(app, ping_interval=5, ping_timeout=10)
CORS(app)
'''
dbconnect = psql.connect(user="postgres",
                              password="26071999papa",
                              host="localhost",
                              port="5432",
                              database="sensor")
cur = psql.cursor()
cur.execute("""CREATE TABLE esp1
               tgl DATE NOT NULL,
               time TIME NOT NULL,
               temp1 VARCHAR(50),
               hum1 VARCHAR(50),
               kwh1 VARCHAR(50),
            """
            )
psql.commit()
psql.close()
'''
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("45856/esp8266/sensors",0)
   #  client.subscribe("/esp8266/humidity")
   #  client.subscribe("/esp8266/kwh")

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
   #socketio.emit('my variable')
   print("Received message '" + str(message.payload) + "' on topic '"
      + message.topic + "' with QoS " + str(message.qos))
   '''
   if message.topic == "/esp8266/temperature":
      on_message.temperature1 = str(message.payload.decode('utf-8'))
      print("temperature update " + on_message.temperature1)
      socketio.emit('dht_temperature', {'data': message.payload})
   if message.topic == "/esp8266/humidity":
      on_message.humidity1 = str(message.payload.decode('utf-8'))
      print("humidity update " +  on_message.humidity1)
      socketio.emit('dht_humidity', {'data': message.payload})
   if message.topic == "/esp8266/kwh":
      on_message.kwh1 = str(message.payload.decode('utf-8'))
      print("kwh update " +  on_message.kwh1)
      socketio.emit('energy_kwh', {'data': message.payload})
   '''
   if message.topic == "45856/esp8266/sensors":
      esp1 = str(message.payload.decode('utf-8'))
      print('received esp1 ', type(esp1))
      esp1_conv = json.loads(esp1)
      print('convert esp1 ', type(esp1_conv))
      print(f'esp1_conv: temp1 {esp1_conv["temperature1"]} --- hum1 {esp1_conv["humidity1"]} --- kwh1 {esp1_conv["kwh1"]}')
      print(type(esp1_conv['temperature1']), type(esp1_conv['humidity1']), type(esp1_conv['kwh1']))
      # socketio.emit('dht_temperature', {'data': esp1_conv["temperature1"]})
      # socketio.emit('dht_humidity', {'data': esp1_conv["humidity1"]})
      # socketio.emit('energy_kwh', {'data': esp1_conv["kwh1"]})
      socketio.emit('sensor1', {'data': message.payload})

      # csv write
      with open('./static/sensor2.csv', mode='a'):
         with open('./static/sensor2.csv', mode='r+', newline='') as file:
            reader = csv.reader(file, delimiter=",")
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            tgl = datetime.now()
            #header = ['tgl','wkt','temp','hum','energy']
            #row = [tgl.strftime("%x"),tgl.strftime("%X"),esp1_conv["temperature1"],esp1_conv["humidity1"],esp1_conv["kwh1"]]
            header = ['datetime','temp','hum','energy']
            row = [tgl.strftime("%Y-%m-%d %X"), esp1_conv["temperature1"], esp1_conv["humidity1"], esp1_conv["kwh1"]]
            
            print(f'file opened: {esp1_conv["temperature1"]} --- {esp1_conv["humidity1"]} --- {esp1_conv["kwh1"]} --- {tgl}')
            #way to write to csv file
            print(enumerate(reader))
            rowcount = sum(1 for num in reader)     #row count
            if rowcount == 0:
               writer.writerow(header)
               print('header written, row count:',rowcount)
            writer.writerow(row)
            print("row written, row count",rowcount)
         
'''
data = [datetime.date(), datetime.time(), on_message.temperature1, on_message.humidity1, on_message.kwh1]
cur.execute('INSERT TO esp1 (tgl,time,temp1,hum1,kwh1')
'''


# initialize mqtt broker
mqttc=mqtt.Client(client_id="capstone")
#broker = 'localhost'
broker = 'mqtt.lunar-smart.com'
port = 8883
username = 'lunar'
password = 'smartsystem'
print("mqtt broker initialized")


# launch mqtt
mqttc.username_pw_set(username, password) #set user pass
#mqttc=mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(broker,port,60)
mqttc.loop_start()
print("mqtt launched")


'''
# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'GPIO 4', 'board' : 'esp8266', 'topic' : 'esp8266/4', 'state' : 'False'},
   5 : {'name' : 'GPIO 5', 'board' : 'esp8266', 'topic' : 'esp8266/5', 'state' : 'False'}
   }

# Put the pin dictionary into the template data dictionary:
templateData = {
   'pins' : pins
   }
'''
@app.route("/")
def main():
   # Pass the template data into the template main_csv_socket.html and return it to the user
   return render_template('main_apexcharts.html', async_mode=socketio.async_mode)
"""
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<board>/<changePin>/<action>")
def action(board, changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   devicePin = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "1" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"1")
      pins[changePin]['state'] = 'True'

   if action == "0" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"0")
      pins[changePin]['state'] = 'False'

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }
   return render_template('main_csv_socket2.html', **templateData)
"""
@socketio.on('my event')
def handle_my_custom_event(json):
   print('received json data here: ' + str(json))
'''
@socketio.on('my event1')
def handle_my_temperature(json):
   print('received json temperature here: ' + str(json))

@socketio.on('my event2')
def handle_my_humidity(json):
   print('received json humidity here: ' + str(json))

@socketio.on('my event3')
def handle_my_kwh(json):
   print('received json humidity here: ' + str(json))
'''
@socketio.on('my sensor')
def handle_my_kwh(json):
   print('received json sensor here: ' + str(json))

def OnExitApp():
    print("exit Flask application")
atexit.register(OnExitApp)

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8080, debug=True)