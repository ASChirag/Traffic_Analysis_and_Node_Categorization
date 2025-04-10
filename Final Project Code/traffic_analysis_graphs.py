import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the data into a pandas DataFrame
df_traffic = pd.read_csv("data.txt", delimiter="\t")

# Drop any missing values (if present)
df_traffic.dropna(inplace=True)

# Convert categorical columns into numerical representations where necessary
df_encoded = df_traffic.copy()
df_encoded["protocol_type"] = df_encoded["protocol_type"].astype("category").cat.codes

# Plot 1: Traffic Volume Over Time (using src_bytes as a proxy for volume)
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_traffic, x=df_traffic.index, y="src_bytes", marker="o", color="b")
plt.xlabel("Time (Index)")
plt.ylabel("Traffic Volume (Bytes)")
plt.title("Traffic Volume Over Time", fontsize=12, fontweight='bold')

# Save the traffic volume plot
traffic_volume_path = "static/images/traffic_volume_over_time.png"
plt.savefig(traffic_volume_path)
plt.close()

# Plot 2: Protocol Usage Distribution (Pie Chart)
plt.figure(figsize=(8, 6))
df_traffic["protocol_type"].value_counts().plot.pie(autopct="%1.1f%%", cmap="coolwarm", startangle=90)
plt.title("Protocol Usage Distribution")
plt.title("Protocol Usage Distribution", fontsize=12, fontweight='bold')
plt.ylabel("")

# Save the protocol distribution pie chart
protocol_pie_path = "static/images/protocol_usage_distribution.png"
plt.savefig(protocol_pie_path)
plt.close()

# Plot 3: Scatter Plot of Traffic Volume vs. Packet Size
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_traffic, x="packet_size", y="src_bytes", hue="protocol_type", palette="viridis")
plt.xlabel("Packet Size")
plt.ylabel("Traffic Volume (Bytes)")
plt.title("Traffic Volume vs. Packet Size")
plt.title("Traffic Volume Over Time", fontsize=12, fontweight='bold')
# Save the scatter plot
scatter_plot_path = "static/images/traffic_volume_vs_packets.png"
plt.savefig(scatter_plot_path)
plt.close()

# Plot 4: Histogram of Connection Duration (Peak Traffic Hours Approximation)
plt.figure(figsize=(10, 6))
sns.histplot(df_traffic["connection_duration"], bins=20, kde=True, color="skyblue")
plt.xlabel("Connection Duration (Seconds)")
plt.ylabel("Count")
plt.title("Distribution of Connection Duration", fontsize=12, fontweight='bold')

# Save the histogram
histogram_path = "static/images/connection_duration_distribution.png"
plt.savefig(histogram_path)
plt.close()

# Return the paths of the saved images
traffic_volume_path, protocol_pie_path, scatter_plot_path, histogram_path
