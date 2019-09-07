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

#
sinkFinal = context.socket(zmq.PULL)
sinkFinal.bind("tcp://*:5556")





# Function to create a hash in hexacode
def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()

# Function to generate random hash with blockchain features
def generation(challenge, size = 25):
    answer = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                      for x in range(size))
    attempt = challenge + answer
    return attempt, answer



print("Press Enter when the workers are ready: ")
_ = input()
print("Sending tasks to workers…")

# The first message is "0" and signals start of batch
sink.send(b'0')


# This is the last hash
challenge = (hashString("CS-rocks!")).encode()
found = ("False").encode()

#while not found:

#print("")
while True:
    if (found.decode() == "True"):
        worker.send_multipart([challenge,found])
        #worker.send_multipart([challenge,found])
        break
    worker.send_multipart([challenge,found])
    found = sinkFinal.recv()
    #print (found.decode())


# Give 0MQ time to deliver
time.sleep(1)