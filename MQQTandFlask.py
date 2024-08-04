
# ===========================================================================================
# This was written by Warren Sutton on 3 Aug 2024
# the program is an example of how a program can subscribe to an MQTT topic
# and have the result displayed on a Webpage using Flask.
# To achieve this the program makes use of threading. Threading is required because the 
# program effectively has two concurrent loops. 
# One loop allows for the subscription to the MQTT topic (which is run in the worker function 
# as a separate thread). The main program runs the Flask app. This allows the 
# code in the worker function to keep running while the website runs.
# ============================================================================================
import paho.mqtt.client as mqtt
import time
import threading
from flask import Flask

app = Flask(__name__)

# The my_temp variable is a global variable that can be updated by both the code in the thread
# which subscribes to the MQTT broker topic and read by the code which creates the website.
my_temp = "not yet known"

# This function is very simple and allows the display of the temperature which the MQTT
# subscription receives
@app.route('/')
def hello_world():
    return f'The temperature is: {my_temp}'

# This function is called when the MQTT client subscription receives data from the 
# MQTT broker
def on_message(client, userdata, message):
    global my_temp
    my_temp = str(message.payload.decode("utf-8"))
    print("received message: " ,my_temp)

# The following MQTT related code including the 'worker()' function allow the program
# to receive data from the 'mqttBroker' assigned and from the subscribed topic.
# There may be better ways to implement this functionality.However, this was tested 
# with paho-mqtt 2.1.0 and worked.
mqttBroker ="broker.hivemq.com"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def worker():
    client.connect(mqttBroker)
    client.subscribe("tempTom")
    client.on_message=on_message
    # The 'loop_forever' is blocking code and if it did not run in a separate thread
    # the program would not be able to launch Flask website, as it would be stuck
    # on this line forever. 
    client.loop_forever()

# The following line of code launches the broker subscription (the 'worker' function).
# The use of 'daemon=True' means that this thread is finishes when the main program
# (website) is terminated.
threading.Thread(target=worker, daemon=True).start()

# The following allows the Flask website to commence running 
if __name__ == '__main__':
    app.run()
