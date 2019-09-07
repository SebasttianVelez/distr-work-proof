import zmq
import random
import time
import string
import hashlib

context = zmq.Context()

# Socket to receive messages on
workers = context.socket(zmq.PULL)
workers.bind("tcp://*:5558")


# Socket with test
fan = context.socket(zmq.PUSH)
fan.connect("tcp://localhost:5556")

#fan.send_string("test")

# Function to create a hash in hexacode
def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()





# Wait for start of batch
s = workers.recv()

# Start our clock now

# Process 100 confirmations
while True:
    answer, found = workers.recv_multipart()
    fan.send_string(str(found.decode()))
    #print (found)
    if(str(found.decode()) == "True"):
        fan.send_string(str(found.decode()))
        break

print (hashString(answer.decode()))