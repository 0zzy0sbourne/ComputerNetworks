import json

class DistanceVectorRouting:
    def __init__(self, graph):
      self.graph = graph
      self.nodes = list(graph.keys())
      self.distance_vectors = {node: {dest: float('inf') for dest in self.nodes} for node in self.nodes}
      self.forwarding_tables = {node: {dest: None for dest in self.nodes} for node in self.nodes}

    def initialize_distance_vectors(self):
        for node in self.nodes:
            self.distance_vectors[node][node] = 0

    def initialize_forwarding_tables(self):
        for node in self.nodes:
            for neighbor in self.graph[node]:
                self.forwarding_tables[node][neighbor] = neighbor

    def exchange_distance_vectors(self):
        for node in self.nodes:
            for neighbor in self.graph[node]:
                self.send_distance_vector(node, neighbor)

    def send_distance_vector(self, source, destination):
        # Simulate sending the distance vector from source to destination
        self.graph[destination][source] = self.distance_vectors[source].copy()

    def update_distance_vectors(self):
        changes = False
        for node in self.nodes:
            for neighbor in self.graph[node]:
                if self.update_distance_vector(node, neighbor):
                    changes = True
        return changes

    def update_distance_vector(self, node, neighbor):
        # Simulate receiving the distance vector from neighbor to node
        self.distance_vectors[node][neighbor] = self.graph[neighbor][node][node]

        # Update the distance vector of node
        for destination in self.nodes:
            if destination == node:
                continue

            # Calculate the distance from node to destination via neighbor
            distance = self.distance_vectors[node][neighbor] + self.graph[neighbor][destination][destination]

            # If the distance is shorter than the current distance, update the distance vector
            if distance < self.distance_vectors[node][destination]:
                self.distance_vectors[node][destination] = distance
                self.forwarding_tables[node][destination] = self.forwarding_tables[node][neighbor]

                return True

        return False
    

    def run(self):
        self.initialize_distance_vectors()
        self.initialize_forwarding_tables()

        iteration = 1
        while True:
            print(f"Iteration {iteration}")
            self.exchange_distance_vectors()
            changes = self.update_distance_vectors()

            self.print_state()

            if not changes:
                break

            iteration += 1

    def print_state(self):
        for node in self.nodes:
            print(f"Node {node}:")
            print(f"Distance Vector: {self.distance_vectors[node]}")
            print(f"Forwarding Table: {self.forwarding_tables[node]}")
            print()

def parse_json_topology(file_path):
  with open(file_path, 'r') as file:
      data = json.load(file)

  # Create a dictionary to map channel_id to data_rate
  channel_data_rates = {channel['channel_id']: int(channel['data_rate']) for channel in data['channels']}

  # Initialize an empty graph
  graph = {}

  # Populate the graph with connections from the JSON data
  for connection in data['connections']:
      source = connection['source_id']
      destination = connection['destination_id']
      channel = connection['channel_id']

      if source not in graph:
          graph[source] = {}

      # Use the data rate as the weight of the edge in the graph
      graph[source][destination] = channel_data_rates[channel]

  return graph


# Example usage:
graph = parse_json_topology('output.txt_1.json')
dv_router = DistanceVectorRouting(graph)
dv_router.run()
