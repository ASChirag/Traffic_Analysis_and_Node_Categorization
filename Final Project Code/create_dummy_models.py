import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
import numpy as np

# Create dummy models
traffic_model = RandomForestClassifier(n_estimators=10)
node_model = RandomForestClassifier(n_estimators=10)
anomaly_model = IsolationForest(n_estimators=10)

# Train models with dummy data
X_traffic = np.random.rand(100, 4)  # 4 features for traffic analysis
y_traffic = np.random.randint(0, 2, 100)  # Binary classification
traffic_model.fit(X_traffic, y_traffic)

X_node = np.random.rand(100, 6)  # 6 features for node categorization
y_node = np.random.randint(0, 5, 100)  # 5 categories
node_model.fit(X_node, y_node)

X_anomaly = np.random.rand(100, 5)  # 5 features for anomaly detection
anomaly_model.fit(X_anomaly)

# Save models
joblib.dump(traffic_model, 'models/traffic_model.joblib')
joblib.dump(node_model, 'models/node_model.joblib')
joblib.dump(anomaly_model, 'models/anomaly_model.joblib')

print("Dummy models created successfully!") 