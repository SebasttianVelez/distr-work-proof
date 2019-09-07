import zmq
import random
import time
import string
import hashlib

context = zmq.Context()

# Socket to receive messages on
fan = context.socket(zmq.PULL)
fan.connect("tcp://localhost:5557")

# Socket to send messages to
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

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

def proofOfWork(challenge):
# Process tasks forever
    found = False
    attempts = 0
    attempt, answer = generation(challenge, 64)
    print(attempt)
    hash = hashString(attempt)
    if hash.startswith('0000'):
        found = True
        print(hash)
    attempts += 1
    print(attempts)
    #print (found)
 
    return answer, str(found)

# Receive the challenge of Fan
#Time 1 worker : 53,77
#Time 2 workers :

challenge, found = fan.recv_multipart()
while True:

    if (found == "True"):
        sink.send_multipart([answer.encode(), found.encode()])
        break
    else:
        answer, found = proofOfWork(challenge.decode())
        sink.send_multipart([answer.encode(), found.encode()])
    # Send results to sink