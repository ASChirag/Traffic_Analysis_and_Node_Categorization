import numpy as np
import pandas as pd

def generate_data(file_path, num_rows=500):
    np.random.seed(42)

    packet_size = np.random.randint(40, 1500, num_rows)  # Packet size in bytes
    connection_duration = np.random.uniform(0.1, 10.0, num_rows)  # Duration in seconds
    src_bytes = np.random.randint(500, 50000, num_rows)  # Data sent from source
    protocol_type = np.random.choice(['TCP', 'UDP', 'HTTP'], num_rows)  # Network protocol
    is_malicious = np.random.randint(0, 2, num_rows)  # 1 = Malicious, 0 = Normal

    data = pd.DataFrame({
        'packet_size': packet_size,
        'connection_duration': connection_duration,
        'src_bytes': src_bytes,
        'protocol_type': protocol_type,
        'is_malicious': is_malicious
    })

    # Save as tab-separated file
    data.to_csv(file_path, sep='\t', index=False)

if __name__ == "__main__":
    file_path = 'data.txt'  # Keep using data.txt
    generate_data(file_path)
    print(f"Data generated and saved to {file_path}")
