# Paxos_Algorithm
Implement Paxos Consensus Algorithm 

Programmed by Sohaibssb as a part of my master research about "Methods of Syncretization Data in Distribution System" at Bauman University, Moscow. Start Summer 28/7/2023.

------------------

Paxos is a distributed consensus algorithm designed to help a group of nodes in a distributed system agree on a single value or outcome, even in the presence of failures and network partitions. It was introduced by Leslie Lamport in 1989 and has become a fundamental concept in distributed systems.

The primary goal of Paxos is to achieve consensus among multiple nodes in an asynchronous network, where nodes may fail or experience communication delays. The algorithm works through a series of voting rounds to ensure that a majority of nodes agree on a proposed value, even if some nodes are faulty or unresponsive.

The Paxos algorithm operates in three main phases:

    1- Prepare Phase: A node (proposer) sends a prepare request to all other nodes (acceptors) with a unique proposal number (also called ballot number). The acceptors respond with the highest proposal number they have seen (if any), indicating that they have already promised to accept a value.

    2- Accept Phase: If the proposer receives responses from a majority of nodes (acceptors) with no higher proposal number, it can proceed to propose a value. The proposer sends an accept request to the acceptors, asking them to accept the proposed value.

    3- Learn Phase: Once a value has been accepted by a majority of nodes, it becomes the agreed-upon value and is considered the consensus. The consensus value is then learned by all nodes in the system, ensuring that all correct nodes eventually agree on the same value.

------------------

Libraries and tchnologies used in this program:

ZeroMQ (zmq): ZeroMQ is a lightweight messaging library used for message passing and communication between different nodes.

JSON (json): JSON is a lightweight data interchange format used to serialize and deserialize data.
