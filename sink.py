import zmq

context = zmq.Context()

# Socket to receive messages on
workers = context.socket(zmq.PULL)
workers.bind("tcp://*:5558")


# Wait for start of batch
s = workers.recv()

answer = workers.recv_string()
print (answer)