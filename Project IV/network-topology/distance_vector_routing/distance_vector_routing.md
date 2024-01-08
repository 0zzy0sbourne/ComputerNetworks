# Router Script (Distance Vector Routing)

## Overview

This script implements a Distance Vector Routing algorithm for routers. It utilizes a threaded approach for running the routing algorithm, monitoring links with neighboring routers, and updating the routing table.

## Features

- **Distance Vector Routing Algorithm:** Implements a basic Distance Vector Routing algorithm for routing information exchange.
- **Threaded Execution:** Utilizes threads for concurrently running the routing algorithm and monitoring links.
- **UDP Socket Communication:** Uses UDP sockets for communication between routers.
- **Routing Table Updates:** Periodically updates routing tables based on received distance vectors.

## Usage

1. Install the required dependencies using the following command:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the script:

    ```bash
    python router.py
    ```

3. Provide the necessary input files and configurations as per the script requirements.

## File Structure

- `router.py`: Main script implementing the Distance Vector Routing algorithm.
- `output.txt_1.json`: Example input JSON file containing network topology information.
- `data/scenario-1`: Directory containing router information files.

## Dependencies

- Python
- Watchdog
- NetworkX
