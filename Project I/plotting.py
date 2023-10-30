import pandas as pd
import matplotlib.pyplot as plt

# Define your data
data = {
    'Destination': [
        "comu.edu.tr",
        "uludag.edu.tr",
        "ege.edu.tr",
        "kayseri.edu.tr",
        "boun.edu.tr",
        "gantep.edu.tr",
        "akdeniz.edu.tr",
        "sabanciuniv.edu",
        "ku.edu.tr",
        "metu.edu"
    ],
    'Minimum Delay': [1903, 1525, 1064, 1043, 867, 955, 915, 887, 832, 578],
    'Maximum Delay': [9682, 4514, 1840, 5088, 1158, 4200, 3703, 1369, 1211, 1751],
    'Average Delay': [3273.9, 1973.3, 1289.3, 1565.0, 967.3, 1393.0, 1333.3, 1021.6, 1010.0, 750.3]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Sort the DataFrame by Average Delay in ascending order
df = df.sort_values(by='Average Delay')

# Create subplots for Minimum, Maximum, and Average Delays
fig, axs = plt.subplots(3, figsize=(10, 15))

# Plot Minimum Delays
axs[0].barh(df['Destination'], df['Minimum Delay'], color='blue')
axs[0].set_xlabel('Minimum Delay (ms)')
axs[0].set_title('Minimum Delay to Destinations')

# Plot Maximum Delays
axs[1].barh(df['Destination'], df['Maximum Delay'], color='red')
axs[1].set_xlabel('Maximum Delay (ms)')
axs[1].set_title('Maximum Delay to Destinations')

# Plot Average Delays
axs[2].barh(df['Destination'], df['Average Delay'], color='green')
axs[2].set_xlabel('Average Delay (ms)')
axs[2].set_title('Average Delay to Destinations')

plt.tight_layout()

# Save the plot as an image file
plt.savefig("traceroute_delays_sunday_0100.png")

# Show the plot
plt.show()
