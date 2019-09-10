import zmq
import random
import time
import string
import hashlib

context = zmq.Context()

# Socket to receive messages on
workers = context.socket(zmq.PULL)
workers.bind("tcp://*:5558")

# Function to create a hash in hexacode
def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()

# Wait for start of batch
s = workers.recv()

# Start our clock now

# Process 100 confirmations
answer = workers.recv_string()


print (hashString(answer))