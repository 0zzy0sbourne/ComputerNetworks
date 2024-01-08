## Generating Router Information

After creating the network topology JSON, use the `generate_router_information.py` script to generate router_information.dat files. This script takes the network topology JSON as input and converts it to .dat files, placing them in the `data/` folder.

```bash
python generate_router_information.py -json [network_topology_file]
```

## Running the Application

Once you have the `router_information.dat` files, run the `ClientApp.py` script with the following command:

```bash
python ClientApp.py -n [router_name] -i [router_ip] -p [router_port] -f [router_information] -t [timeout] -w [www]
```

(e.g.)
```bash
 python ClientApp.py -n a -i 127.0.0.1 -p 8080 -f router_information.dat -t 15
```