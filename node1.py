import zmq
import time
import random
import json
import threading
 #"UpdateCode2"
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
        json_message = json.dumps({"message_type": message_type, "data": data})
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
        return json.loads(json_message)

    def send_value_to_node(self, value, target_node_id):
        self.send_message("value", {"value": value}, target_node_id)

    def run(self):
        list1 = []
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
            print("Te 1")
            print(received_value)
            print(data)
            list1.append(received_value)
            print("The list is")
            print(list1)

            self.send_message("ACK", None)

if __name__ == "__main__":
    node_id = 1
    total_nodes = 2
    print("\nNode 1 is Working\n")
    node = PaxosNode(node_id, total_nodes)

    # Start a separate thread to run the node's run() method
    node_thread = threading.Thread(target=node.run)
    node_thread.start()

    while True:
        pp = input("Enter a value (or 'exit' to stop): ")
        if pp.lower() == 'exit':
            break

        pp = int(pp)
        node.send_value_to_node(pp, 2)

    # Wait for the node thread to finish
    node_thread.join()
