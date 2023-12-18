# Import the json module to read and write JSON files
import json

# Define a constant for infinity
INF = float("inf")

# Define a function to read the network topology from a JSON file
def read_topology(filename):
  # Open the file and load the JSON data
  with open(filename, "r") as f:
    data = json.load(f)
  # Return the data as a dictionary
  return data

# Define a function to write the distance vector table to a JSON file
def write_table(filename, table):
  # Open the file and dump the JSON data
  with open(filename, "w") as f:
    json.dump(table, f, indent=4)
  # Print a message
  print(f"Distance vector table written to {filename}")

# Define a function to initialize the distance vector table
def initialize_table(topology, source):
  # Create an empty dictionary
  table = {}
  # Loop through the nodes in the topology
  for node in topology:
    # Initialize the distance and the next hop for each node
    if node == source:
      # The distance and the next hop for the source node are itself
      table[node] = {"distance": 0, "next_hop": node}
    else:
      # The distance and the next hop for the other nodes are infinity and None
      table[node] = {"distance": INF, "next_hop": None}
  # Return the table as a dictionary
  return table

# Define a function to update the distance vector table using the Bellman-Ford algorithm
def update_table(table, topology, source):
  # Create a copy of the table
  new_table = table.copy()
  # Loop through the nodes in the topology
  for node in topology:
    # Loop through the neighbors of the node
    for neighbor in topology[node]:
      # Get the cost of the link between the node and the neighbor
      cost = topology[node][neighbor]
      # Get the distance and the next hop of the node from the table
      distance = table[node]["distance"]
      next_hop = table[node]["next_hop"]
      # Get the distance and the next hop of the neighbor from the table
      neighbor_distance = table[neighbor]["distance"]
      neighbor_next_hop = table[neighbor]["next_hop"]
      # Check if the distance to the neighbor can be improved by going through the node
      if neighbor_distance > distance + cost:
        # Update the distance and the next hop of the neighbor in the new table
        new_table[neighbor]["distance"] = distance + cost
        new_table[neighbor]["next_hop"] = node
  # Return the new table as a dictionary
  return new_table

# Define a function to check if two tables are equal
def equal_tables(table1, table2):
  # Loop through the keys in the table1
  for key in table1:
    # Check if the values for the key are different in the table2
    if table1[key] != table2[key]:
      # Return False
      return False
  # Return True
  return True

# Define the name of the source node
source = "A"

# Define the name of the JSON file that contains the network topology
topology_file = "topology.json"

# Define the name of the JSON file that will store the distance vector table
table_file = "table.json"

# Read the network topology from the JSON file
topology = read_topology(topology_file)

# Initialize the distance vector table
table = initialize_table(topology, source)

# Print the initial table
print("Initial table:")
write_table(table_file, table)

# Create a flag to indicate if the table has changed
changed = True

# Loop until the table does not change
while changed:
  # Update the table using the Bellman-Ford algorithm
  new_table = update_table(table, topology, source)
  # Check if the new table is equal to the old table
  if equal_tables(new_table, table):
    # Set the flag to False
    changed = False
  else:
    # Set the table to the new table
    table = new_table
    # Print the updated table
    print("Updated table:")
    write_table(table_file, table)

# Print the final table
print("Final table:")
write_table(table_file, table)
