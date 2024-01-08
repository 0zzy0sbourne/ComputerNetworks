import sys
import os
import signal
import atexit
import argparse

from distance_vector_routing.router import Router
from distance_vector_routing.router import FileNotExistError
from distance_vector_routing.router import RouterError

from link_state_routing.link_state import LinkStateRouting

# Global variables
router = None

# Shut down the router on Ctrl+C or on exiting from application
def shutdown(signal=None, frame=None):
    if router:
        router.stop()
        sys.exit(1)
signal.signal(signal.SIGINT, shutdown)
# atexit.register(shutdown)

def run_distance_vector_routing(**args):
    global router

    # Arguments
    routerName = args["router_name"]
    routerIP = args["router_ip"]
    routerPort = args["router_port"]
    routerInformation = args["router_information"]
    timeout = args["timeout"]
    www = args["www"]

    # Create 'Router' object
    router = Router(routerName, routerIP, routerPort, timeout, www)

    try:
        # Start running the Distance Vector Routing algorithm
        router.start(routerInformation)
    except FileNotExistError as e:
        print("Path not exist!")
        print(e)
    except RouterError as e:
        print("Unexpected exception in router!")
        print(e)
    except Exception as e:
        print("Unexpected exception!")
        print(e)


def run_link_state_routing(**args):
    # Additional logic to run Link State Routing
    # Use the provided arguments or add any other necessary setup

    try:
        # Create 'LinkStateRouting' object
        link_state_router = LinkStateRouting(
            router_name=args["router_name"],
            router_ip=args["router_ip"],
            router_port=args["router_port"],
            router_information=args["router_information"],
            timeout=args["timeout"],
            www=args["www"]
        )

        # Start running the Link State Routing algorithm
        link_state_router.run()
    except Exception as e:
        print("Unexpected exception in Link State Routing!")
        print(e)


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description='Distance Vector Routing algorithm',
                                     prog='python \
                                           ClientApp.py \
                                           -n <router_name> \
                                           -i <router_ip> \
                                           -p <router_port> \
                                           -f <router_information> \
                                           -t <timeout> \
                                           -w <www>')

    parser.add_argument("-n", "--router_name", type=str, default="a",
                        help="Router name, default: a")
    parser.add_argument("-i", "--router_ip", type=str, default="127.0.0.1",
                        help="Router IP, default: 127.0.0.1")
    parser.add_argument("-p", "--router_port", type=int, default=8080,
                        help="Router port, default: 8080")
    parser.add_argument("-f", "--router_information", type=str, default="router_information.dat",
                        help="Router information, default: router_information.dat")
    parser.add_argument("-t", "--timeout", type=int, default=15,
                        help="Timeout, default: 15")
    parser.add_argument("-w", "--www", type=str, default=os.path.join(os.getcwd(), "router_info_generator"),
                        help="Path consisting of router information, default: /<Current Working Directory>/generate_router_information/")

    # Read user inputs
    args = vars(parser.parse_args())

    # Run Distance Vector Routing
#     run_distance_vector_routing(**args)

    # Run Link State Routing after running the Distance Vector Routing
    run_link_state_routing(**args)