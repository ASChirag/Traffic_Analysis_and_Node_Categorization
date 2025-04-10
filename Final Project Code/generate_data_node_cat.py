import numpy as np
import pandas as pd

def generate_node_data(file_path, num_rows=500):
    np.random.seed(42)

    ip_address_range = np.random.choice(['192.168.x.x', '10.x.x.x', '172.16.x.x', 'External'], num_rows)
    protocol_type = np.random.choice(['TCP', 'UDP', 'HTTP', 'ICMP'], num_rows)
    packets_sent = np.random.randint(100, 5000, num_rows)
    device_type = np.random.choice(['PC', 'Server', 'Router', 'IoT Device'], num_rows)
    traffic_volume = np.random.randint(1000, 100000, num_rows)
    connection_frequency = np.random.randint(1, 100, num_rows)

    node_category = np.random.choice(['Normal User', 'Server Node', 'Router/Switch', 'IoT Device', 'Malicious Node'], num_rows)

    data = pd.DataFrame({
        'ip_address_range': ip_address_range,
        'protocol_type': protocol_type,
        'packets_sent': packets_sent,
        'device_type': device_type,
        'traffic_volume': traffic_volume,
        'connection_frequency': connection_frequency,
        'node_category': node_category  # Target column
    })

    # Save as a tab-separated file
    data.to_csv(file_path, sep='\t', index=False)

if __name__ == "__main__":
    file_path = 'node_data.txt'
    generate_node_data(file_path)
    print(f"Node categorization data generated and saved to {file_path}")
