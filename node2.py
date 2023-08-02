import zmq
import time
import random
import json
import sys
import threading
import queue

class PaxosNode:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes

        self.prepare_n = None
        self.accepted_n = None
        self.accepted_value = None
        self.promised_n = None
        self.accepted_nack = False

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://127.0.0.1:555{node_id}")


    def send_message(self, message_type, data=None, target_node_id=None):
        json_message = json.dumps({"message_type": message_type,"data":data})
        if target_node_id is not None:
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect(f"tcp://127.0.0.1:555{target_node_id}")
            socket.send_string(json_message)
            socket.recv_string()
        else: 
            self.socket.send_string(json_message)

    def receive_message(self):
        json_message = self.socket.recv_string()

        print("I rec num")

        return json.loads(json_message)
    
    def send_value_to_node(self, value, target_node_id):
        self.send_message("value", {"value": value}, target_node_id)

    def run(self):
        received_value = None
        while True:
            message = self.receive_message()

            if "message_type" in message:
                message_type = message["message_type"]
                data = message["data"]

                if message_type == "value":
                    received_value = data["value"]
                    print(f"Node {self.node_id} received value: {received_value}")

            # Simulate some work before responding to messages
            time.sleep(random.uniform(0.1, 0.5))

            # Respond to the received message
            print("Te 2")
            print(received_value)
            print(data)
            self.send_message("ACK", None)
            node.send_value_to_node(received_value, 1)
         

if __name__ == "__main__":
    node_id = 2
    total_nodes = 2

    node = PaxosNode(node_id, total_nodes)

    # Start a separate thread to run the node's run() method
    node_thread = threading.Thread(target=node.run)
    node_thread.start()

    # Keep the main thread alive to listen for input
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break