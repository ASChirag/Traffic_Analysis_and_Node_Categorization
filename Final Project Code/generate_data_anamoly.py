import numpy as np
import pandas as pd

def generate_anomaly_data(file_path, num_rows=1000, anomaly_fraction=0.05):
    np.random.seed(42)

    # Normal data generation
    packets_sent = np.random.randint(100, 5000, num_rows)
    traffic_volume = np.random.randint(1000, 100000, num_rows)
    connection_duration = np.random.uniform(0.5, 10.0, num_rows)
    connection_frequency = np.random.randint(1, 100, num_rows)
    protocol_type = np.random.choice(['TCP', 'UDP', 'HTTP', 'ICMP'], num_rows)
    src_bytes = np.random.randint(50, 5000, num_rows)
    packet_size = np.random.randint(40, 1500, num_rows)

    # Generate labels (0 - Normal, 1 - Anomaly)
    labels = np.zeros(num_rows)

    # Introduce anomalies (5% of data by default)
    num_anomalies = int(num_rows * anomaly_fraction)
    anomaly_indices = np.random.choice(num_rows, num_anomalies, replace=False)

    # Inject anomalous data
    packets_sent[anomaly_indices] = np.random.randint(8000, 20000, num_anomalies)
    traffic_volume[anomaly_indices] = np.random.randint(200000, 500000, num_anomalies)
    connection_duration[anomaly_indices] = np.random.uniform(50.0, 200.0, num_anomalies)
    connection_frequency[anomaly_indices] = np.random.randint(150, 300, num_anomalies)
    src_bytes[anomaly_indices] = np.random.randint(10000, 50000, num_anomalies)
    packet_size[anomaly_indices] = np.random.randint(2000, 5000, num_anomalies)
    
    # Mark these as anomalies
    labels[anomaly_indices] = 1

    # Create DataFrame
    data = pd.DataFrame({
        'packets_sent': packets_sent,
        'traffic_volume': traffic_volume,
        'connection_duration': connection_duration,
        'connection_frequency': connection_frequency,
        'protocol_type': protocol_type,
        'src_bytes': src_bytes,
        'packet_size': packet_size,
        'label': labels  # 0 for Normal, 1 for Anomaly
    })

    # Save data
    data.to_csv(file_path, sep='\t', index=False)

if __name__ == "__main__":
    file_path = 'anomaly_data.txt'
    generate_anomaly_data(file_path)
    print(f"Anomaly detection data generated and saved to {file_path}")
