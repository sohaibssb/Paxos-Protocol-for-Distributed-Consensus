import zmq
import time
import random
import json
import threading
import zmq.error

 #"UpdateCode3 - Done"
class PaxosNode:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://127.0.0.1:555{node_id}")
        self.received_value = None
#///////////////////////////////////////////////////////////////////////////////////
    def send_value_to_node(self, value, target_node_id):
        self.send_message("value", {"value": value}, target_node_id)
        #return self.received_values.get(target_node_id)

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

    def run(self):
        while True:
            message = self.receive_message()

            if "message_type" in message:
                message_type = message["message_type"]
                data = message["data"]

                if message_type == "value":
                    self.received_value = data["value"]  # Store the received value

            self.send_message("ACK", None)

    def get_received_value(self):
        return self.received_value




if __name__ == "__main__":
    node_id = 1
    total_nodes = 3
    print("\nУзел 1 работает\n")
    node = PaxosNode(node_id, total_nodes)

    node_thread = threading.Thread(target=node.run)
    node_thread.start()

    i = 0
    list1 = []

    while True:
        try:
            print("--------------------------------------------------")
            proposal = int(input("Пожалуйста, введите свои идентификационные номера: "))
        except ValueError:
            print("Error !!")
            print("Пожалуйста, введите только цифры")
            continue

        proposal = int(proposal)

        #///////////////////////////////////
        print("\n")
        print(f"Номер предложения: {proposal}")
        list1.append(proposal)
        print("\nСписок номеров предложений:")
        print(list1)
        #///////////////////////////////////
        node.send_value_to_node(proposal, 2)
        Vnode2 = node.get_received_value()
        #print("Test Received value from node 2:", Vnode2)
        node.send_value_to_node(proposal, 3)
        Vnode3 = node.get_received_value()
        #print("Test Received value from node 3:", Vnode3)
        #///////////////////////////////////
        accept = 0
        promise = 0
        npromise = 0
        iaccept = 0
        inaccept = 0

        if i == 0:
                promise = 1
                print(f"Узел 1, обещанная стоимость: {proposal}")
        elif max(list1) == proposal:
                promise = 1
                print(f"Узел 1, обещанная стоимость: {proposal}")
        else:
                npromise = 1
                print(f"Узел 1, не обещанная ценность: {proposal}")

        if Vnode2 == 1:
                iaccept = iaccept + 1
                print(f"Узел 2, обещанная стоимость: {proposal}")
        else:
                inaccept = inaccept + 1
                print(f"Узел 2, не обещанная ценность: {proposal}")

        if Vnode3 == 1:
                iaccept = iaccept + 1
                print(f"Узел 3, обещанная стоимость: {proposal}")
        else:
                inaccept = inaccept + 1
                print(f"Узел 3, не обещанная ценность: {proposal}")

        if iaccept > inaccept:
                accept = proposal
                print("\n")
                print(f"Номер предложения: {accept} --> Принял")
                print("\n")
        else:
                inaccept = proposal
                print("\n")
                print(f"Номер предложения: {inaccept} --> не принимаются")
                print("\n")

        i = i + 1

    # Wait for the node thread to finish
    node_thread.join()
