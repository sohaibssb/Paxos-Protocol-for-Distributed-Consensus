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

        #self.prepare_n = None
        #self.accepted_n = None
        #self.accepted_value = None
        #self.promised_n = None
        #self.accepted_nack = False

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
        i = 0
        accept = 0
        while True:
            message = self.receive_message()

            if "message_type" in message:
                message_type = message["message_type"]
                data = message["data"]

                if message_type == "value":
                    received_value = data["value"]
                    #print(f"Узел {self.node_id} полученное значение: {received_value}")

            # Simulate some work before responding to messages
            # time.sleep(random.uniform(0.1, 0.5))

            # Respond to the received message
            print("\n")
            print(f"Номер предложения: {proposal}")
            #print(data)
            list1.append(proposal)
            print("\nСписок номеров предложений:")
            print(list1)

            #/////////////////////////////////////////////////////////////////////////////
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

            if received_value == 1:
                iaccept = iaccept + 1
                print(f"Узел 2, обещанная стоимость: {proposal}")
            else:
                inaccept = inaccept + 1
                print(f"Узел 2, не обещанная ценность: {proposal}")

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

            #/////////////////////////////////////////////////////////////////////////////

            self.send_message("ACK", None)

if __name__ == "__main__":
    node_id = 1
    total_nodes = 2
    print("\nУзел 1 работает\n")
    node = PaxosNode(node_id, total_nodes)

    node_thread = threading.Thread(target=node.run)
    node_thread.start()

    while True:
        try:
            print("--------------------------------------------------")
            proposal = int(input("Пожалуйста, введите свои идентификационные номера: "))
        except ValueError:
            print("Error !!")
            print("Пожалуйста, введите только цифры")
            continue

        proposal = int(proposal)
        node.send_value_to_node(proposal, 2)

    # Wait for the node thread to finish
    node_thread.join()
