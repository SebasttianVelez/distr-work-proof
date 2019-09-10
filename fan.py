import zmq
import random
import time
import string
import hashlib


context = zmq.Context()


# Socket to send messages on WORKERS
worker = context.socket(zmq.PUSH)
worker.bind("tcp://*:5557")

# Socket with direct access to the sink: used to syncronize start of batch
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

# Function to create a hash in hexacode
def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()

# Function to generate random hash with blockchain features
_ = input("Press Enter when the workers are ready: ")
print("Sending tasks to workers…")

# The first message is "0" and signals start of batch
sink.send(b'0')


# This is the last hash
challenge = hashString("CS-rocks!")


for i in range(3):
    worker.send_string(challenge)