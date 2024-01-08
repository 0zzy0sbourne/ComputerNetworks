import os
import time
import json
import logging
import heapq
import socket
import struct
import select
from threading import Thread, Lock, Event
from collections import namedtuple

import networkx as nx

from distance_vector_routing.router import Router

# Set logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s LINK STATE ROUTING [%(levelname)s] %(message)s',)
log = logging.getLogger()

# Lock for synchronized access to 'LinkStateRouting'
LOCK = Lock()

# Constants
INFINITY = float('inf')


class FileNotExistError(Exception):
    pass


class RouterError(Exception):
    pass


class LinkStateRouting(Thread):
    """
    Thread for running Link State Routing algorithm.
    """

    PACKET = namedtuple("Packet", ["Router",
                                   "Checksum",
                                   "SequenceNumber",
                                   "LSP",
                                   "Payload"])

    def __init__(self,
                 routerName,
                 routerSocket,
                 routerIP,
                 routerPort,
                 topologyGraph,
                 timeout=15,
                 threadName="LinkStateRouting",
                 bufferSize=2048):
        Thread.__init__(self)
        self._stopevent = Event()
        self.routerName = routerName
        self.routerSocket = routerSocket
        self.routerIP = routerIP
        self.routerPort = routerPort
        self.topologyGraph = topologyGraph
        self.timeout = timeout
        self.threadName = threadName
        self.bufferSize = bufferSize

    def run(self):
        """
        Start running Link State Routing algorithm.
        """
        sequenceNumber = 1

        while not self._stopevent.isSet():
            # Send Link State Packet (LSP) to all routers
            self.send_lsp(sequenceNumber)

            # Listen for incoming LSPs from other routers
            start_time = time.time()
            while True:
                # If timeout, stop listening on socket
                if (time.time() - start_time) > self.timeout:
                    break

                ready = select.select([self.routerSocket], [], [], self.timeout)
                if not ready[0]:
                    break

                try:
                    receivedPacket, receiverAddress = self.routerSocket.recvfrom(self.bufferSize)
                except Exception as e:
                    log.error("[%s] Could not receive UDP packet!", self.threadName)
                    log.debug(e)
                    raise RouterError("Receiving UDP packet failed!")

                receivedPacket = self.parse_lsp(receivedPacket)

                # Check whether the received packet is not corrupt
                if self.corrupt_lsp(receivedPacket):
                    log.warning("[%s] Discarding corrupt received LSP!", self.threadName)
                    continue

                # Update topology graph based on received LSP
                log.info("[%s] Updating topology graph", self.threadName)
                self.update_topology(receivedPacket)

            sequenceNumber += 1

    def send_lsp(self, sequenceNumber):
        """
        Send Link State Packet (LSP) to all routers.
        """
        lsp = self.create_lsp(sequenceNumber)

        for neighborRouter, routerAddress in self.topologyGraph.neighbors(self.routerName):
            self.rdt_send(lsp, routerAddress)

    def create_lsp(self, sequenceNumber):
        """
        Create Link State Packet (LSP).
        """
        lsp = {
            "router_name": self.routerName,
            "sequence_number": sequenceNumber,
            "neighbors": {}
        }

        for neighborRouter, routerAddress in self.topologyGraph.neighbors(self.routerName):
            cost = self.topologyGraph[self.routerName][neighborRouter]["cost"]
            lsp["neighbors"][neighborRouter] = {"cost": cost}

        return lsp

    def rdt_send(self, lsp, routerAddress):
        """
        Reliable data transfer for LSP.
        """
        rawLSP = self.make_pkt(lsp)

        try:
            self.routerSocket.sendto(rawLSP, routerAddress)
        except Exception as e:
            log.error("[%s] Could not send UDP packet!", self.threadName)
            log.debug(e)
            raise RouterError("Sending UDP packet to %s:%d failed!"
                              % (routerAddress[0], routerAddress[1]))

    def make_pkt(self, lsp):
        """
        Create a raw LSP.
        """
        payload = json.dumps(lsp)
        router = struct.pack('=1s', self.routerName.encode('iso-8859-1'))
        payloadSize = struct.pack('=I', len(payload))
        checksum = struct.pack('=H', self.checksum(payload))
        payload = struct.pack('='+str(len(payload))+'s', payload.encode())
        rawLSP = router + payloadSize + checksum + payload

        return rawLSP

    def parse_lsp(self, receivedPacket):
        """
        Parse LSP from the received packet.
        """
        router = struct.unpack('=1s', receivedPacket[0:1])[0]
        payloadSize = struct.unpack('=I', receivedPacket[1:5])[0]
        checksum = struct.unpack('=H', receivedPacket[5:7])[0]
        payload = struct.unpack('='+str(payloadSize)+'s', receivedPacket[7:])[0]

        content = json.loads(payload.decode())
        lsp = LinkStateRouting.PACKET(Router=router,
                                      Checksum=checksum,
                                      SequenceNumber=content["sequence_number"],
                                      LSP=content,
                                      Payload=payload)

        return lsp

    def corrupt_lsp(self, receivedPacket):
        """
        Check whether the received LSP is corrupt or not.
        """
        computedChecksum = self.checksum(receivedPacket.Payload)

        if computedChecksum != receivedPacket.Checksum:
            return True
        else:
            return False

    def checksum(self, data):
        """
        Compute and return a checksum of the given payload data.
        """
        if (len(data) % 2) != 0:
            data += "0"

        sum = 0
        for i in range(0, len(data), 2):
            data16 = ord(data[i]) + (ord(data[i+1]) << 8)
            sum = self.carry_around_add(sum, data16)

        return ~sum & 0xffff

    def carry_around_add(self, sum, data16):
        """
        Helper function for carry around add.
        """
        sum = sum + data16
        return (sum & 0xffff) + (sum >> 16)

    def update_topology(self, receivedPacket):
        """
        Update topology graph based on received LSP.
        """
        sourceRouter = receivedPacket.Router
        sequenceNumber = receivedPacket.SequenceNumber
        lsp = receivedPacket.LSP

        with LOCK:
            # Update or add the source router to the topology graph
            if not self.topologyGraph.has_node(sourceRouter):
                self.topologyGraph.add_node(sourceRouter)

            # Check if the received LSP is newer than the stored LSP
            if not self.topologyGraph.has_edge(self.routerName, sourceRouter) or \
                    self.topologyGraph[self.routerName][sourceRouter]["sequence_number"] < sequenceNumber:
                self.topologyGraph[self.routerName][sourceRouter] = {
                    "sequence_number": sequenceNumber,
                    "cost": 0  # Set the cost to 0 for direct connections
                }

            # Update or add neighbors to the topology graph
            for neighbor, neighborInfo in lsp["neighbors"].items():
                if not self.topologyGraph.has_node(neighbor):
                    self.topologyGraph.add_node(neighbor)

                if not self.topologyGraph.has_edge(sourceRouter, neighbor) or \
                        self.topologyGraph[sourceRouter][neighbor]["cost"] != neighborInfo["cost"]:
                    self.topologyGraph.add_edge(sourceRouter, neighbor, cost=neighborInfo["cost"])

    def compute_shortest_paths(self):
        """
        Compute shortest paths and update forwarding tables.
        """
        with LOCK:
            forwarding_tables = {}
            packet_transmission_delay = 0
            total_cost = 0
            run_time = 0

            for destination in self.topologyGraph.nodes():
                if destination != self.routerName:
                    path, cost = nx.single_source_dijkstra(self.topologyGraph, self.routerName, destination)

                    # Update forwarding tables
                    forwarding_tables[destination] = {"path": path, "cost": cost}

                    # Calculate packet transmission delay
                    packet_transmission_delay += cost

                    # Update total cost
                    total_cost += cost

            # Calculate runtime
            run_time = time.time() - self.start_time

        return forwarding_tables, packet_transmission_delay, total_cost, run_time

    def terminate(self, timeout=5):
        """
        Terminate the thread.
        """
        self._stopevent.set()
        Thread.join(self, timeout)


if __name__ == "__main__":
    input_json_file = "output.txt_1.json"
    with open(input_json_file, "r") as f:
        network_topology = json.load(f)

    routers = {}
    topology_graph = nx.Graph()

    for link in network_topology['links']:
        topology_graph.add_edge(link['from'], link['to'], cost=link['cost'])

    for node in network_topology['nodes']:
        router = Router(
            routerName=node["node_id"],
            routerIP="127.0.0.1",
            timeout=15,
            www=os.path.join(os.getcwd(), "data", "scenario-1")
        )
        routers[node["node_id"]] = router

    link_state_routing = LinkStateRouting(
        routerName=node["node_id"],
        routerSocket=routers[node["node_id"]].routerSocket,
        routerIP="127.0.0.1",
        routerPort=8080,
        topologyGraph=topology_graph
    )

    # Start Link State Routing algorithm
    link_state_routing.start()

    # Wait for the algorithm to run
    time.sleep(30)  # Adjust the duration as needed

    # Terminate the Link State Routing algorithm
    link_state_routing.terminate()

    # Compute and print results
    forwarding_tables, packet_transmission_delay, total_cost, run_time = link_state_routing.compute_shortest_paths()

    print("Forwarding Tables:")
    for destination, info in forwarding_tables.items():
        print(f"{node['node_id']} to {destination}: {info['path']} (Cost: {info['cost']})")

    print(f"Packet Transmission Delay (End-to-End): {packet_transmission_delay}")
    print(f"Total Cost of the Path Chosen: {total_cost}")
    print(f"Run Time of the Algorithm: {run_time}")
    print(f"Number of Hop Counts (End-to-End): {total_cost}")  # Assuming cost represents hop counts
