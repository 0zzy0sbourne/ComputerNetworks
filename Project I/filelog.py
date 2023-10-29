import re
import subprocess
import schedule
import time

# Define the destinations that we want to test
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
repetitions = {"first_setup": 10, "second_setup": 10, "third_setup": 10}
# Define the times for each setup
setup_times = {"first_setup": "10:54:30", "second_setup": "02:00:00", "third_setup": "06:00:00"}

# Function to run traceroute for a destination
def run_traceroute(destination, repetitions, output_file):
    with open(output_file, "a") as f:  # Append mode
        f.write(f"Executing traceroute for {destination}...\n")

    total_delays = []
    total_delay = 0  # Initialize total_delay for each run
    for _ in range(repetitions):
        try:
            traceroute_command = ["tracert", "-w", "5", destination]
            tracert_output = subprocess.check_output(traceroute_command).decode("utf-8")

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

# Output file to write the log
output_file = "traceroute_log.txt"

# Manually start each setup
for setup, time_to_run in setup_times.items:
    # Wait for the specified time
    current_time = time.strftime("%H:%M:%S")
    while current_time != time_to_run:
        time.sleep(1)
        current_time = time.strftime("%H:%M:%S")
        print(current_time)
    
    print(f"Starting setup for {setup} at {current_time}")
    with open(output_file, "a") as f:  # Append mode
        f.write(f"Starting setup for {setup} at {current_time}\n")
    for destination in destinations:
        run_traceroute(destination, repetitions[setup], output_file)

    print(f"Setup for {setup} completed.")
    with open(output_file, "a") as f:  # Append mode
        f.write(f"Setup for {setup} completed.\n")
