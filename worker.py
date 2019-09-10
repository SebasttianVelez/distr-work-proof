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
sink.connect("udp://localhost:5558")

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
    found = False
    attempts = 0
    while not found:
        attempt, answer = generation(challenge, 64)
        print(attempt)
        hash = hashString(attempt)
        if hash.startswith('00000'):
            found = True
            #print(hash)
        attempts += 1
    #print(attempts)
    return answer, found


found = False
challenge = fan.recv_string()

while not found:
        answer, found = proofOfWork(challenge)
        if found:
            sink.send_string(answer)