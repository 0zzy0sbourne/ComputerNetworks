import re
import subprocess
import time
import threading

# Define the destinations that we want to test
destinations = [
    "boun.edu.tr", 
    "ku.edu.tr", 
    "sabanciuniv.edu",
    "uludag.edu.tr",
    "comu.edu.tr",
    "metu.edu", 
    "ege.edu.tr", 
    "akdeniz.edu.tr",
    "kayseri.edu.tr",
    "gantep.edu.tr"
]

# Define the number of repetitions for each setup
repetitions = {"first_setup": 10, "second_setup": 10, "third_setup": 10}

# Define the times for each setup
setup_times = {"first_setup": "11:00:00", "second_setup": "13:00:00", "third_setup": "15:00:00"}

# Output file to write the log
output_file = "threading_monday_traceroute_log.txt"

# Function to run traceroute for a destination
def run_traceroute(destination, repetitions):
    current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, "a") as f:  # Append mode
        f.write(f"{current_datetime} - Executing traceroute for {destination}...\n")
    
    total_delays = []
    total_delay = 0  # Initialize total_delay for each run
    for _ in range(repetitions):
        try:
            traceroute_command = ["tracert", "-w", "5", destination]
            tracert_output = subprocess.check_output(["tracert", destination]).decode("utf-8")
            with open(output_file, "a") as f:  # Append mode
                f.write(f"Traceroute for {destination}:\n{tracert_output}")

            # Define a regular expression pattern to match delay lines
            delay_pattern = r"(\d+)\s+((?:\d+\s+ms\s*)+)"

            # Search for and extract delay information using the pattern
            delay_matches = re.findall(delay_pattern, tracert_output)

            # Initialize the list to store current delay data
            current_delay_data = []

            # Extract the delay values and add them to the list
            for match in delay_matches:
                hop, delay_values = match
                delay_values = [int(delay.strip('ms')) for delay in delay_values.split() if delay.strip('ms').isdigit()]
                total_delay += sum(delay_values)
                current_delay_data.extend(delay_values)

            with open(output_file, "a") as f:  # Append mode
                f.write(f"Delays for {destination} in the {_+1}st run: {current_delay_data}\n")
                f.write(f"Total delay for {destination} in the {_+1}st run: {total_delay}\n")
        except subprocess.CalledProcessError as e:
            with open(output_file, "a") as f:  # Append mode
                f.write(f"Error executing traceroute for {destination}: {e}\n")
        except Exception as e:
            with open(output_file, "a") as f:  # Append mode
                f.write(f"An error occurred for {destination}: {e}\n")
        total_delays.append(total_delay)
        total_delay = 0

    min_delay = min(total_delays)
    max_delay = max(total_delays)
    avg_delay = sum(total_delays) / len(total_delays)

    with open(output_file, "a") as f:  # Append mode
        f.write(f"Minimum Delay for {destination}: {min_delay} ms\n")
        f.write(f"Maximum Delay for {destination}: {max_delay} ms\n")
        f.write(f"Average Delay for {destination}: {avg_delay} ms\n")

# Manually start each setup using threads for concurrent traceroute execution
for setup, time_to_run in setup_times.items():
    current_time = time.strftime("%H:%M:%S")
    while current_time != time_to_run:
        time.sleep(1)
        current_time = time.strftime("%H:%M:%S")
        print(current_time)
    
    print(f"Starting setup for {setup} at {current_time}")
    
    # Create threads for each destination
    threads = []
    for destination in destinations:
        thread = threading.Thread(target=run_traceroute, args=(destination, repetitions[setup]))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"Setup for {setup} completed.")
