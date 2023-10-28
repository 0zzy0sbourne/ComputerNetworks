import re
import subprocess
import matplotlib.pyplot as plt
import schedule
import time
from tracert_parser import parse_tracert_output
 
# Define the destinations that we want to test
# Government institutions often have static IP addresses and stable server locations.
# destinations = [
#                     "boun.edu.tr", 
#                     "ku.edu.tr", 
#                     "sabancıuniv.edu",
#                     "uludag.edu.tr",
#                     "comu.edu.tr",
#                     "metu.edu", 
#                     "ege.edu.tr", 
#                     "akdeniz.edu.tr",
#                     "kayseri.edu.tr",
#                     "gantep.edu.tr"
#                 ]

destinations = [
                    "boun.edu.tr",
                ]


# Define the number of repetitions for each setup
repetitions = {"first_setup": 2, "second_setup": 10, "third_setup": 10}
# Define the times for each setup
setup_times = {"first_setup": "21:08:00", "second_setup": "20:00:00", "third_setup": "23:00:00"}

# Function to run traceroute for a destination
def run_traceroute(destination, repetitions):
    print("Executing traceroute...\n")
    total_delays = []
    total_delay = 0  # Initialize total_delay for each run
    for _ in range(repetitions):
        try:
            traceroute_command = ["tracert", "-w", "5", destination]
            tracert_output = subprocess.check_output(["tracert", destination]).decode("utf-8")
            print(f"Traceroute for {destination}:\n{tracert_output}")

            # Define a regular expression pattern to match delay lines
            # delay_pattern = r"(\d+)\s+([\d.]+) ms"
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

            print(f"Delays for {destination} şn the {_+1}st run: {current_delay_data}")
            print(f"Total delay for {destination} in the {_+1}st run: {total_delay}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing traceroute for {destination}: {e}")
        except Exception as e:
            print(f"An error occurred for {destination}: {e}")
        total_delays.append(total_delay)
        total_delay = 0

    min_delay = min(total_delays)
    max_delay = max(total_delays)
    avg_delay = sum(total_delays) / len(total_delays)

    print(f"Minimum Delay for {destination}:", min_delay, "ms")
    print(f"Maximum Delay for {destination}:", max_delay, "ms")
    print(f"Average Delay for {destination}:", avg_delay, "ms")
    

# Manually start each setup
for setup, time_to_run in setup_times.items():
    # Wait for the specified time
    current_time = time.strftime("%H:%M:%S")
    while current_time != time_to_run:
        time.sleep(1)
        current_time = time.strftime("%H:%M:%S")
        print(current_time)
    
    print(f"Starting setup for {setup} at {current_time}")
    for destination in destinations:
        run_traceroute(destination, repetitions[setup])

    print(f"Setup for {setup} completed.")













































































def run_script():
    # Initialize dictionaries to store delay data
    print("Executing the main function...")
    delay_data = {destination: {time: [] for time in times_of_day} for destination in destinations}

    # Simulate running the project for a week
    for destination in destinations:
        for time in times_of_day: 
            # Run the tracert command and capture the output
            print("Calculating the traceroute...")
            try:
                tracert_output = subprocess.check_output(["tracert", destination]).decode("utf-8")
                print(tracert_output)
            except subprocess.CalledProcessError as e:
                print(f"Error executing tracert: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")
            
            # Define a regular expression pattern to match delay lines
            # delay_pattern = r"(\d+)\s+([\w.-]+)\s+([\d.]+)ms"
            # Define a regular expression pattern to match delay lines
            delay_pattern = r"(\d+)\s+ms"

            # Search for and extract delay information using the pattern
            delay_matches = re.findall(delay_pattern, tracert_output)
            
            # Initialize the dictionary to store current delay data
            # current_delay_data = {}
            # for match in delay_matches:
            #     hop, ip_address, delay = match
            #     current_delay_data[int(hop)] = {"ip_address": ip_address, "delay": float(delay)}
            
            # Initialize the list to store current delay data
            current_delay_data = []
            
            # Iterate through matches and append the delays
            for match in delay_matches:
                delay = int(match)
                current_delay_data.append(delay)
            # Append the delay data to the delay_data dictionary
            delay_data[destination][time] = current_delay_data
            
            # # Update the delay data dictionary with the current data
            # for hop, data in current_delay_data.items():
            #     delay_data[destination][time].append(data)

    # Print delay data for this specific run
    print(delay_data)
    
    # Generate graphs for delays
    for destination in destinations:
        for time in times_of_day:
            plt.plot(delay_data[destinations][time], label=f"{destination} - {time}")
            plt.xlabel("Day")
            plt.ylabel("Delay (ms)")
            plt.title("Delay Over a Week")
            plt.legend()

    # Display or save the graphs
    plt.show()  # Display the graphs
    # plt.savefig("delay_graph.png")  # Save the graphs to a file
    
# # Define the times of the day for testing (morning, noon, and evening) with actual dates and times
# times_of_day = ["15:48:00",]

# def print_message(time):
#     print(f"the time is {time}")

# # Schedule the script to run at specific dates and times
# for time_to_run in times_of_day:
#     schedule.every().day.at(time_to_run).do(run_script)

# # Run the scheduled tasks
# while True:
#     schedule.run_pending()
#     time.sleep(1)
