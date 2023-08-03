import zmq
import time
import random
import json
import threading

class PaxosNode:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes

        #self.prepare_n = None
        #self.accepted_n = None
        #self.accepted_value = None
        #self.promised_n = None
        #self.accepted_nack = False

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://127.0.0.1:555{node_id}")
        self.send_socket = self.context.socket(zmq.REQ)
        self.send_socket.connect(f"tcp://127.0.0.1:5551")  # Change the target node_id as needed

    def send_message(self, message_type, data=None, target_node_id=None):
        json_message = json.dumps({"message_type": message_type, "data": data})
        if target_node_id is not None:
            self.send_socket.send_string(json_message)
            self.send_socket.recv_string()
        else:
            self.socket.send_string(json_message)

    def receive_message(self):
        json_message = self.socket.recv_string()
        return json.loads(json_message)

    def send_value_to_node(self, value, target_node_id):
        self.send_message("value", {"value": value}, target_node_id)

    def run(self):
        received_value = None
        list2 = []
        i = 0
        while True:
            message = self.receive_message()

            if "message_type" in message:
                message_type = message["message_type"]
                data = message["data"]

                if message_type == "value":
                    received_value = data["value"]
                    print(f"Узел {self.node_id} полученное значение: {received_value}")

            # Simulate some work before responding to messages
            #time.sleep(random.uniform(0.1, 0.5))

            # Respond to the received message
            #print("\nНомер предложения:")
            #print(received_value)
            #print(data)
            list2.append(received_value)
            print("\nСписок номеров предложений:")
            print(list2)
            print("\n")

            #/////////////////////////////////////////////////////////////////////////////
            promise = 0
            npromise = 0

            if i == 0:
                promise = 1
                print(f"Узел 2, обещанная стоимость: {received_value}")
            elif max(list2) == received_value:
                promise = 1
                print(f"Узел 2, обещанная стоимость: {received_value}")
            else:
                npromise = 1
                print(f"Узел 2, не обещанная ценность: {received_value}")

            if promise == 1:
                self.send_value_to_node(1, 1)
            else:
                self.send_value_to_node(0, 1)

            i = i + 1
            print("\n-------------------------------")
            #/////////////////////////////////////////////////////////////////////////////

            self.send_message("ACK", None)

if __name__ == "__main__":
    node_id = 2
    total_nodes = 2
    print("\nУзел 2 работает\n")
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
