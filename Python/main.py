# Import necessary libraries
import paho.mqtt.client as mqttClient
import time
import zmq
import datetime
import signal
import pmt
import json
import base64
import requests
import binascii
import socket
import threading
from multiprocessing import Process, Pipe
import logging
import queue
import xmlrpc.client

# Enable or disable debug console
Debug_Console = False

# Initialize counter variables
Count_1, Count_2, Count_3, Count_4, Count_5, Count_6 = 0,0,0,0,0,0

# Class for colorful terminal output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Set up logging
logging.basicConfig(level=logging.DEBUG,
                      format='[%(levelname)s] (%(threadName)-9s) %(message)s',)

# Set up xmlrpc server for gnuradio
server = xmlrpc.client.ServerProxy("http://localhost:8089/RPC2")

# Set up the thread pool
thread_pool = []
max_threads = 5
thread_queue = queue.Queue()

# Set up zmq context and sockets for transmission
context = zmq.Context()
sock = context.socket(zmq.PUSH)
sock.bind("tcp://127.0.0.1:5555")

sock2 = context.socket(zmq.PUSH)
sock2.bind("tcp://127.0.0.1:5554")


# Function to send LoRa message
def send_message_lora(phyPayload, delay, frequency, spreadingfactor):
	Delay_offset_Sf7 = 0.196 #Delay for SF7 
	Delay_offset_Sf12 = 0.155 #Delay for SF12

	# Initialize the list with your elements
	counts = [Count_1, Count_2, Count_3, Count_4, Count_5, Count_6]

	# Find the index of the largest element
	max_index = counts.index(max(counts))

	formatt = base64.b64decode(phyPayload).hex()
	formatted = formatt + ','
	
	# Set the frequency variable
	server.set_sink_freq2(frequency)

	end_time = time.perf_counter_ns()
	elapsed_time_ns = end_time - counts[max_index]
	elapsed_time_s = elapsed_time_ns / 1_000_000_000
	if Debug_Console == True:
		logging.debug(f"Elapsed time: {elapsed_time_s:.6f} seconds")

	if spreadingfactor == 12:
		delay = int(delay) - Delay_offset_Sf12 - elapsed_time_s
		time.sleep(delay)
		sock2.send(bytes(formatted, encoding='utf-8'))
	
	if spreadingfactor == 7: 
		delay = int(delay) - Delay_offset_Sf7 - elapsed_time_s
		time.sleep(delay)
		
		#Experimental
		print("SF7 - Waiting: ", delay)
		for x in range(5):
			time.sleep(0.02)
			sock.send(bytes(formatted, encoding='utf-8'))	

	print(f"{bcolors.OKBLUE}\nSending packet to GNURadio{bcolors.ENDC}")
	print(f"{bcolors.WARNING}	PHYPayload: {bcolors.ENDC}", phyPayload, "\n")
	print(f"{bcolors.WARNING}	Delay: {bcolors.ENDC}{delay:.4f}{bcolors.WARNING} - Frequency: {bcolors.ENDC}{frequency}{bcolors.WARNING} - SF: {bcolors.ENDC}{spreadingfactor}")

# Mqtt from chirpstack		
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print(f"{bcolors.OKGREEN} Connected to broker{bcolors.ENDC}")
		global Connected
		Connected = True

	else:
		print(f"{bcolors.WARNING} Connection failed{bcolors.ENDC}")

# Function to deconstruct received message and call send_message_lora
def deconstruct_message(message_payload):
	data = json.loads(message_payload)

	phyPayload = data['items'][0]['phyPayload']
	try:
		delay = data['items'][0]['txInfoLegacy']['delayTimingInfo']['delay']
		delay = delay[0]
	except:
		delay = 2

	try:
		frequency = data['items'][0]['txInfoLegacy']['frequency']
	except:
		frequency = 868100000
		
	try:
		spreadingfactor = data['items'][0]['txInfoLegacy']['loraModulationInfo']['spreadingFactor']
	except: 
		spreadingfactor = 12
		
	return send_message_lora(phyPayload, delay, frequency, spreadingfactor)

# Function to handle MQTT message
def on_message(client, userdata, message):
	deconstruct_message(message.payload)

# Function to send packet to network
def send_packet_nettwork(data, freq, sf):
	if Debug_Console == True:
		logging.debug('Starting')

	# Convert the binary data to hex, hex_data = received packet
	hex_data = data.hex()
	
	
	# Convert the hex data to base64
	base64_data = base64.b64encode(bytes.fromhex(hex_data)).decode()

	# Define the packet structure
	PACKET_VERSION = 2
	PUSH_DATA_IDENTIFIER = 0x00

	# Gateway EUI64 ID
	GATEWAY_EUI64 = "5c7e869fc5cbf9e4"

	# Get localtime with ISO 8601 format
	obj = time.localtime()
	localtime = time.strftime("%Y-%m-%dT%H:%M:%SZ", obj)

	# Example JSON payload
	json_payload = {"rxpk":[
		{
			"time":str(localtime),
			"freq":freq,
			"stat":1,
			"modu":"LORA",
			"datr":"SF" + str(sf) + "BW125",
			"codr":"4/5",
			"size":32,
			"data":str(base64_data)
		}
		]
	}
	json_payload_string = json.dumps(json_payload)

	# Encode the packet
	random_token = b'\x02\xD0'
	json_payload_bytes = json_payload_string.encode('utf-8')
	gateway_id = binascii.unhexlify(GATEWAY_EUI64)  # Convert EUI64 to bytes
	packet = bytes([PACKET_VERSION]) + random_token + bytes([PUSH_DATA_IDENTIFIER]) + gateway_id + json_payload_bytes 
	#packet_base64 = binascii.b2a_base64(packet, newline=False)

	# Send the packet to the server
	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		s.sendto(packet, ('localhost', 1700))
	# Print out some information about the packet being sent
	print(f"{bcolors.OKBLUE}\nSending packet to Network Server{bcolors.ENDC}")
	print(f"{bcolors.WARNING}	Base64 Data: {bcolors.ENDC}", base64_data)
	if Debug_Console == True:
		logging.debug('Finished')

# Listener function for threads
def listener1():
	global Count_1
	consumer_receiver = context.socket(zmq.PULL)
	consumer_receiver.connect("tcp://127.0.0.1:5556")
	while True:
		data = consumer_receiver.recv()
		freq = 868.100000
		sf = 12
		Count_1 = time.perf_counter_ns()
		process_thread = threading.Thread(target=send_packet_nettwork, args=(data, freq, sf))
		process_thread.start()

def listener2():
	global Count_2
	consumer_receiver = context.socket(zmq.PULL)
	consumer_receiver.connect("tcp://127.0.0.1:5559")
	while True:
		data = consumer_receiver.recv()
		freq = 868.100000
		sf = 7
		Count_2 = time.perf_counter_ns()
		process_thread = threading.Thread(target=send_packet_nettwork, args=(data, freq, sf))
		process_thread.start()
		
def listener3():
	global Count_3
	consumer_receiver = context.socket(zmq.PULL)
	consumer_receiver.connect("tcp://127.0.0.1:5557")
	while True:
		data = consumer_receiver.recv()
		freq = 868.300000
		sf = 12
		Count_3 = time.perf_counter_ns()
		process_thread = threading.Thread(target=send_packet_nettwork, args=(data, freq, sf))
		process_thread.start()
		
def listener4():
	global Count_4
	consumer_receiver = context.socket(zmq.PULL)
	consumer_receiver.connect("tcp://127.0.0.1:5560")
	while True:
		data = consumer_receiver.recv()
		freq = 868.300000
		sf = 7
		Count_4 = time.perf_counter_ns()
		process_thread = threading.Thread(target=send_packet_nettwork, args=(data, freq, sf))
		process_thread.start()

def listener5():
	global Count_5
	consumer_receiver = context.socket(zmq.PULL)
	consumer_receiver.connect("tcp://127.0.0.1:5558")
	while True:
		data = consumer_receiver.recv()
		freq = 868.500000
		sf = 12
		Count_5 = time.perf_counter_ns()
		process_thread = threading.Thread(target=send_packet_nettwork, args=(data, freq, sf))
		process_thread.start()

def listener6():
	global Count_6
	consumer_receiver = context.socket(zmq.PULL)
	consumer_receiver.connect("tcp://127.0.0.1:5561")
	while True:
		data = consumer_receiver.recv()
		freq = 868.500000
		sf = 7
		Count_6 = time.perf_counter_ns()
		process_thread = threading.Thread(target=send_packet_nettwork, args=(data, freq, sf))
		process_thread.start()


Connected = False   #global variable for the state of the connection

broker_address= "localhost"         #Broker address
port = 1883                         #Broker port
user = ""                           #Connection username
password = ""                       #Connection password

client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback

client.connect(broker_address, port=port)          #connect to broker

client.loop_start()          #start the loop

while Connected != True:     #Wait for connection
	time.sleep(0.1)

client.subscribe("+/gateway/+/command/down")


t1 = threading.Thread(target=listener1)
t2 = threading.Thread(target=listener2)
t3 = threading.Thread(target=listener3)
t4 = threading.Thread(target=listener4)
t5 = threading.Thread(target=listener5)
t6 = threading.Thread(target=listener6)
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
	
