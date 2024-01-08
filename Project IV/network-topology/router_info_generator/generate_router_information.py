# import json
# import os

# # Load the JSON file
# with open('output_1.json', 'r') as f:
#     data = json.load(f)

# # Create a dictionary to map channel_id to data_rate
# channel_data_rate = {channel['channel_id']: channel['data_rate'] for channel in data['channels']}

# # Create a dictionary to map node_id to a list of its connections
# node_connections = {}
# for connection in data['connections']:
#     if connection['source_id'] not in node_connections:
#         node_connections[connection['source_id']] = []
#     node_connections[connection['source_id']].append({
#         'Router Name': connection['destination_id'],
#         'Link Cost': channel_data_rate[connection['channel_id']],
#         'IP Address': '127.0.0.1',  # Assuming all nodes are on localhost
#         'Port': '8080',  # Assuming all nodes are on port 8080
#     })

# # Create the data folder if it does not exist
# if not os.path.exists('data'):
#     os.makedirs('data')

# # Write the router_information.dat files
# for node_id, connections in node_connections.items():
#     with open(f'../data/{node_id}_router_information.dat', 'w') as f:
#         f.write(str(len(connections)) + '\n')
#         for connection in connections:
#             f.write(' '.join([str(value) for value in connection.values()]) + '\n')


import json

def generate_router_information(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract nodes information
    nodes = data.get("nodes", [])

    # Create router information in the desired format
    router_information = []

    for node in nodes:
        if node.get("node_type") == "router":
            interfaces = node.get("interfaces", [])
            if interfaces:
                interface_id = interfaces[0].get("interface_id", "interface1")
                router_id = node.get("node_id", "")
                x_coord = node.get("x-coord", "0")
                y_coord = node.get("y-coord", "0")
                router_info = f"{router_id} 2.0 127.0.0.1 808{ord(router_id[-1]) - ord('a') + 1} # ({x_coord}, {y_coord})"
                router_information.append(router_info)

    # Save router information to a file
    output_file = "router_information.dat"
    with open(output_file, 'w') as output:
        for router_info in router_information:
            output.write(router_info + '\n')

    print(f"Router information generated and saved to {output_file}")

if __name__ == "__main__":
    json_file_path = "output_1.json"
    generate_router_information(json_file_path)
