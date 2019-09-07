import zmq
import random
import time
import string
import hashlib

context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

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

found = False

def proofOfWork(challenge):
    found = False
    attempts = 0
    while not found:
        attempt, answer = generation(challenge, 64)
        print(attempt)
        hash = hashString(attempt)
        if hash.startswith('0000'):
            found = True
            #print(hash)
        attempts += 1
    #print(attempts)
    return answer, found

# Process tasks forever
while not found:
    challenge = receiver.recv()
    answer, found = proofOfWork(challenge.decode())
    sink.send_string(answer)

    # Send results to sink