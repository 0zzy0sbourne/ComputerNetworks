import json
import os

# Load the JSON file
with open('output.txt_1.json', 'r') as f:
    data = json.load(f)

# Create a dictionary to map channel_id to data_rate
channel_data_rate = {channel['channel_id']: channel['data_rate'] for channel in data['channels']}

# Create a dictionary to map node_id to a list of its connections
node_connections = {}
for connection in data['connections']:
    if connection['source_id'] not in node_connections:
        node_connections[connection['source_id']] = []
    node_connections[connection['source_id']].append({
        'Router Name': connection['destination_id'],
        'Link Cost': channel_data_rate[connection['channel_id']],
        'IP Address': '127.0.0.1',  # Assuming all nodes are on localhost
        'Port': '8080',  # Assuming all nodes are on port 8080
    })

# Create the data folder if it does not exist
if not os.path.exists('data'):
    os.makedirs('data')

# Write the router_information.dat files
for node_id, connections in node_connections.items():
    with open(f'data/{node_id}_router_information.dat', 'w') as f:
        f.write(str(len(connections)) + '\n')
        for connection in connections:
            f.write(' '.join([str(value) for value in connection.values()]) + '\n')