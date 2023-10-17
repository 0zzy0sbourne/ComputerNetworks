import subprocess
import matplotlib.pyplot as plt
import schedule
import time
from tracert_parser import parse_tracert_output

# Define the locations that we want to test
# Educational and government institutions often have static IP addresses and stable server locations.
locations = ["harvard.edu", "stanfor.edu", "ox.ac.uk"]

def run_script():
    # Initialize dictionaries to store delay data
    print("run_script is called")
    delay_data = {location: {time: [] for time in times_of_day} for location in locations}

    # Simulate running the project for a week
    for day in range(7):
        for location in locations:
            for time in times_of_day:
                # Run the tracert command and capture the output
                destination = location
                tracert_output = subprocess.check_output(["tracert", destination]).decode("utf-8")

                # Parse the tracert output to extract delay information
                current_delay_data = parse_tracert_output(tracert_output)

                # Update the delay data dictionary with the current data
                for hop, data in current_delay_data.items():
                    delay_data[location][time].append(data)

    # Generate graphs for delays
    for location in locations:
        for time in times_of_day:
            plt.plot(delay_data[location][time], label=f"{location} - {time}")
            plt.xlabel("Day")
            plt.ylabel("Delay (ms)")
            plt.title("Delay Over a Week")
            plt.legend()

    # Display or save the graphs
    plt.show()  # Display the graphs
    # plt.savefig("delay_graph.png")  # Save the graphs to a file

# Define the times of the day for testing (morning, noon, and evening) with actual dates and times
times_of_day = ["08:00", "12:00", "18:00", "19:23:30"]

def print_message(time):
    print(f"the time is {time}")

# Schedule the script to run at specific dates and times
for time_to_run in times_of_day:
    schedule.every().day.at(time_to_run).do(run_script)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
