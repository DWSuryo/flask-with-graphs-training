import paho.mqtt.client as mqtt
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import eventlet
from datetime import datetime    # show date
import time                      # time
import csv        # for storing data
#import psycopg2 as psql   # PostgreSQL
import json
import atexit

eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'xDsTbiULqIrqXkO_X5kcyg'
socketio = SocketIO(app, ping_interval=5, ping_timeout=10)
CORS(app)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("45856/esp8266/sensors",0)

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
   #socketio.emit('my variable')
   print("Received message '" + str(message.payload) + "' on topic '"
      + message.topic + "' with QoS " + str(message.qos))
   
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


# initialize mqtt broker
mqttc=mqtt.Client(client_id="capstone")
broker = 'localhost'
port = 1883
username = ''
password = ''
print("mqtt broker initialized")

# launch mqtt
mqttc.username_pw_set(username, password) #set user pass
#mqttc=mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(broker,port,60)
mqttc.loop_start()
print("mqtt launched")

@app.route("/")
def main():
   # Pass the template data into the template main_csv_socket.html and return it to the user
   return render_template('main_apexcharts.html', async_mode=socketio.async_mode)

@socketio.on('my event')
def handle_my_custom_event(json):
   print('received json data here: ' + str(json))

@socketio.on('my sensor')
def handle_my_kwh(json):
   print('received json sensor here: ' + str(json))

def OnExitApp():
    print("exit Flask application")
atexit.register(OnExitApp)

if __name__ == "__main__":
   socketio.run(app, host='0.0.0.0', port=8080, debug=True)
