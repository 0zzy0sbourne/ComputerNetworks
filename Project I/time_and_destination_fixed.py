import pandas as pd
import matplotlib.pyplot as plt

# Define the data for each day
data = {
    'Day': ['Friday', 'Saturday', 'Sunday', 'Monday'],
    'Time': ['01:00:00', '01:00:00', '01:00:00', '01:00:00'],
    'Minimum Delay': [600, 620, 578, 590],
    'Maximum Delay': [1650, 1800, 1751, 1700],
    'Average Delay': [725.8, 760.5, 750.3, 735.2]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a bar plot for Average Delays
plt.figure(figsize=(10, 6))
plt.bar(df['Day'], df['Average Delay'], color=['blue', 'green', 'purple', 'red'])
plt.xlabel('Day')
plt.ylabel('Average Delay (ms)')
plt.title('Average Delays for metu.edu at 14:00:00 on Different Days')

# Save the plot as an image file
plt.savefig("traceroute_delays_combined.png")

# Show the plot
plt.show()
