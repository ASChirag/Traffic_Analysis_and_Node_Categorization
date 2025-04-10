import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Convert raw data into a structured dataframe
columns = ["ip_address_range", "protocol_type", "packets_sent", "device_type", 
           "traffic_volume", "connection_frequency", "node_category"]

# Read the node data into a pandas DataFrame
df_nodes = pd.read_csv("node_data.txt", delimiter="\t")

# Drop any rows with missing values (if any)
df_nodes.dropna(inplace=True)

# Convert categorical columns into numerical representations using label encoding
categorical_columns = ["ip_address_range", "protocol_type", "device_type", "node_category"]
df_encoded = df_nodes.copy()

for col in categorical_columns:
    df_encoded[col] = df_encoded[col].astype("category").cat.codes

# Plot node category distribution (Pie Chart)
plt.figure(figsize=(8, 6))
df_nodes["node_category"].value_counts().plot.pie(autopct="%1.1f%%", cmap="coolwarm", startangle=90)
plt.title("Node Category Distribution", fontsize=12, fontweight='bold')
plt.ylabel("")

# Save the pie chart
pie_chart_path = "static/images/node_category_distribution.png"
plt.savefig(pie_chart_path)
plt.close()

# Scatter Plot: Packets Sent vs. Traffic Volume colored by Node Category
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_encoded, x="packets_sent", y="traffic_volume", hue="node_category", palette="viridis")
plt.xlabel("Packets Sent")
plt.ylabel("Traffic Volume")
plt.title("Packets Sent vs. Traffic Volume (Colored by Node Category)", fontsize=12, fontweight='bold')

# Save the scatter plot
scatter_plot_path = "static/images/packets_vs_traffic.png"
plt.savefig(scatter_plot_path)
plt.close()

# Histogram of Connection Frequency
plt.figure(figsize=(10, 6))
sns.histplot(df_encoded["connection_frequency"], bins=20, kde=True, color="skyblue")
plt.xlabel("Connection Frequency")
plt.ylabel("Count")
plt.title("Distribution of Connection Frequency", fontsize=12, fontweight='bold')

# Save the histogram
histogram_path = "static/images/connection_frequency_distribution.png"
plt.savefig(histogram_path)
plt.close()

# Return the generated image paths
pie_chart_path, scatter_plot_path, histogram_path
