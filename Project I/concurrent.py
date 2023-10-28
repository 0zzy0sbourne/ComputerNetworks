import asyncio
import time
import re
import subprocess

# Define the destinations that you want to test
destinations = [
    "boun.edu.tr", 
    "ku.edu.tr", 
    "sabancıuniv.edu",
    "uludag.edu.tr",
    "comu.edu.tr",
    "metu.edu", 
    "ege.edu.tr", 
    "akdeniz.edu.tr",
    "kayseri.edu.tr",
    "gantep.edu.tr"
]

# Define the number of repetitions for each setup
repetitions = {"first_setup": 2, "second_setup": 10, "third_setup": 10}

# Define the times for each setup
setup_times = {"first_setup": "18:18:20", "second_setup": "20:00:00", "third_setup": "23:00:00"}

# Function to run traceroute for a destination
async def run_traceroute_single(destination, setup):
    total_delays = []
    for _ in range(repetitions[setup]):
        try:
            tracert_output = subprocess.check_output(["tracert", destination]).decode("utf-8")
            print(f"Traceroute for {destination}:\n{tracert_output}")
            await asyncio.sleep(2)
            print(f"Traceroute for {destination} in {setup} completed.")
        except Exception as e:
            print(f"Error executing traceroute for {destination} in {setup}: {e}")

# Function to run traceroute for all destinations concurrently within a setup
async def run_traceroute_concurrently(setup):
    print(f"Starting setup for {setup} at {current_time}")
    tasks = [run_traceroute_single(destination, setup) for destination in destinations]
    await asyncio.gather(*tasks)

# Create an event loop
loop = asyncio.get_event_loop()

# Manually start each setup
for setup, time_to_run in setup_times.items():
    current_time = time.strftime("%H:%M:%S")
    while current_time != time_to_run:
        time.sleep(1)
        current_time = time.strftime("%H:%M:%S")
        print(current_time)

    # Run the setup concurrently
    loop.run_until_complete(run_traceroute_concurrently(setup))

# Close the event loop
loop.close()
