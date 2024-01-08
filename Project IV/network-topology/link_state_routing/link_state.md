# Link State Routing Script

## Overview

This script implements a Link State Routing algorithm for managing routing tables in a network. Link State Routing is a type of routing algorithm that relies on each router's understanding of the complete network topology.

## Features

- **Link State Algorithm:** Utilizes the Link State Routing algorithm to calculate the shortest path between routers based on their understanding of the network topology.

- **Forwarding Tables:** The script generates forwarding tables for each node, showcasing the optimal paths to reach other nodes in the network.

- **Packet Transmission Delay:** Calculates the end-to-end packet transmission delay, providing insights into the time it takes for a packet to travel from source to destination.

- **Total Cost of the Path:** Computes the total cost associated with the chosen path between nodes in the network.

- **Hop Counts:** Displays the number of hops required for end-to-end communication between nodes.

- **Run Time:** Provides the execution time of the Link State Routing algorithm.

## Usage

1. **Input Topology:** Ensure that the network topology is represented correctly in the input JSON file.

2. **Run the Script:** Execute the script to initiate the Link State Routing algorithm.

   ```bash
   python link_state_routing.py

## Dependencies

- **NetworkX:** A Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
- **Matplotlib:** A comprehensive library for creating static, animated, and interactive visualizations in Python.

## Installation

Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
