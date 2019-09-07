import zmq
import random
import time
import string
import hashlib

context = zmq.Context()

# Socket to receive messages on
workers = context.socket(zmq.PULL)
workers.bind("tcp://*:5558")


# Wait for start of batch
s = workers.recv()

# Start our clock now

# Process 100 confirmations
for r in range(1):
    s = workers.recv()

    print (s.decode())