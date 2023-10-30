import matplotlib.pyplot as plt

# Data for metu.edu delays
times = ["19:00:00", "21:00:00", "23:00:00"]
average_delays = [110.9, 147.5, 111.0]  # Update with actual average delays
maximum_delays = [149, 297, 193]  # Update with actual maximum delays

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Plot average delays
ax.plot(times, average_delays, marker='o', label='Average Delay (ms)')

# Plot maximum delays
ax.plot(times, maximum_delays, marker='o', label='Maximum Delay (ms)')

# Set plot labels and title
ax.set_xlabel("Time")
ax.set_ylabel("Delay (ms)")
ax.set_title("Metu.edu Delay Analysis (Sunday)")

# Add a legend
ax.legend()

# Show the plot
plt.grid()
plt.show()
