import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import joblib
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ============================
# 📚 Step 1: Read Data from a File
# ============================
def read_data(file_path):
    data = pd.read_csv(file_path, delimiter='\t')
    return data


# ============================
# ✨ Step 2: Data Preprocessing
# ============================
def preprocess_data(data):
    for col in data.columns:
        if data[col].dtype == 'object':  # Handle categorical columns
            if data[col].nunique() <= 10:
                data[col] = LabelEncoder().fit_transform(data[col])
            else:
                data = pd.get_dummies(data, columns=[col], drop_first=True)
    return data


# ============================
# 🎯 Step 3: Feature Extraction
# ============================
def extract_features(data):
    X = data.iloc[:, :-1]  # Features
    y = data.iloc[:, -1]  # Target
    return X, y


# ============================
# 🚀 Step 4: Train ML Model
# ============================
def train_model(X, y=None, model_type="classification"):
    """
    Generalized function to train models for classification and anomaly detection.

    Args:
        X (DataFrame or np.array): Feature matrix.
        y (Series or np.array, optional): Target values for classification models.
        model_type (str): Type of model to train. Options:
            - "classification" for traffic and node categorization.
            - "anomaly" for anomaly detection (unsupervised).

    Returns:
        tuple: Trained model and scaler.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 🎯 Classification Model
    if model_type == "classification":
        if y is None:
            raise ValueError("Target labels (y) are required for classification models.")
        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate Model
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        # Save Report
        with open("report.txt", "a", encoding="utf-8") as f:
            f.write("🔹 Classification Report:\n")
            f.write(report + "\n")
            f.write("\n🔹 Confusion Matrix:\n")
            f.write(np.array2string(conf_matrix) + "\n")

        print(report)
        print("Confusion Matrix:\n", conf_matrix)

    # 🔍 Anomaly Detection Model
    elif model_type == "anomaly":
        model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        model.fit(X_scaled)
        print("✅ Anomaly detection model trained successfully!")

    else:
        raise ValueError("❌ Invalid model type specified! Use 'classification' or 'anomaly'.")

    return model, scaler


# ============================
# 🧠 Step 5: Node Categorization
# ============================
def categorize_nodes(model, scaler, new_data):
    new_data_scaled = scaler.transform(new_data)
    predictions = model.predict(new_data_scaled)

    category_mapping = {
        0: "Normal User",
        1: "Server Node",
        2: "Router/Switch",
        3: "IoT Device",
        4: "Malicious Node"
    }

    categorized_predictions = [category_mapping.get(pred, "Unknown") for pred in predictions]
    return categorized_predictions


# ============================
# 📊 Step 6: Analyze and Save Traffic Data
# ============================
def analyze_traffic(data, predictions):
    data['Category'] = predictions
    data.to_csv("categorized_data.txt", sep='\t', index=False)

    with open("report.txt", "a", encoding="utf-8") as f:
        f.write("\n🔹 First 5 Rows of Categorized Traffic Data:\n")
        f.write(data.head().to_string() + "\n")

    return data


# ============================
# 📈 Step 7: Data Visualization
# ============================
def visualize_data(data):
    sampled_data = data.sample(min(300, len(data)))

    # Pair Plot
    pairplot = sns.pairplot(sampled_data, hue='Category', height=1.5, aspect=1.2)
    pairplot.fig.suptitle("Feature Relationships (Pair Plot)", fontsize=16, fontweight='bold')
    pairplot.fig.subplots_adjust(top=0.95)
    pairplot.savefig('pairplot.png')

    # Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(data.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Feature Correlation Heatmap", fontsize=14, fontweight='bold')
    plt.savefig('heatmap.png', dpi=300)
    plt.close()

    # Bar Chart
    plt.figure(figsize=(8, 6))
    category_counts = data['Category'].value_counts()
    sns.barplot(x=category_counts.index, y=category_counts.values, palette="viridis")
    plt.title("Traffic Category Distribution", fontsize=14, fontweight='bold')
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.savefig('bar_chart.png', dpi=300)
    plt.close()

    print("✅ Plots saved: pairplot.png, heatmap.png, bar_chart.png")


# ============================
# 🔍 Step 8: Anomaly Detection
# ============================
def detect_anomalies(data):
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()

    # Clean unwanted columns
    if 'anomaly' in numeric_columns:
        numeric_columns.remove('anomaly')
    if 'Category' in numeric_columns:
        numeric_columns.remove('Category')

    data_subset = data[numeric_columns]
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_subset)

    # Train Anomaly Detection Model
    model, _ = train_model(data_subset, model_type="anomaly")

    data['Anomaly'] = model.predict(data_scaled)

    anomaly_count = (data['Anomaly'] == -1).sum()
    print(f"🔍 Detected {anomaly_count} anomalies out of {len(data)} records.")
    
    anomalies = data[data['Anomaly'] == -1]
    anomalies.to_csv("anomaly_data.txt", sep='\t', index=False)
    print("✅ Anomalies saved to anomaly_data.txt")

    return data, model


# ============================
# 🎨 Step 9: Visualize Anomalies
# ============================
def visualize_anomalies(data):
    numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()

    if 'Anomaly' in numeric_columns:
        numeric_columns.remove('Anomaly')

    if len(numeric_columns) >= 2:
        x_col, y_col = numeric_columns[:2]

        # Scatter Plot
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[x_col], y=data[y_col], hue=data['Anomaly'], palette={1: 'green', -1: 'red'}, alpha=0.7)
        plt.title(f'Anomaly Detection - {x_col} vs {y_col}', fontsize=14, fontweight='bold')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.legend(['Normal', 'Anomaly'])
        plt.savefig('anomaly_scatter.png')
        plt.close()

    # Pie Chart
    anomaly_counts = data['Anomaly'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(anomaly_counts, labels=['Normal', 'Anomaly'], autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
    plt.title('Anomaly vs Normal Traffic', fontsize=14, fontweight='bold')
    plt.savefig('anomaly_pie_chart.png')
    plt.close()

    print("✅ Anomaly graphs saved: anomaly_scatter.png, anomaly_pie_chart.png")


# ============================
# 🔥 Main Section
# ============================
if __name__ == "__main__":
    # === Traffic Analysis (data.txt) ===
    file_path = 'data.txt'
    data = read_data(file_path)
    data = preprocess_data(data)
    X, y = extract_features(data)
    model, scaler = train_model(X, y, model_type="classification")

    # Traffic Analysis
    full_predictions = categorize_nodes(model, scaler, X)
    analyzed_data = analyze_traffic(data, full_predictions)

    print("Traffic Analysis Results:")
    print(analyzed_data.head())
    joblib.dump(model, "traffic_analysis_model.pkl")
    visualize_data(analyzed_data)

    # === Node Categorization (node_data.txt) ===
    file_path = 'node_data.txt'
    data = read_data(file_path)
    data = preprocess_data(data)
    X, y = extract_features(data)
    node_model, node_scaler = train_model(X, y, model_type="classification")

    # Categorize New Nodes
    node_predictions = categorize_nodes(node_model, node_scaler, X)
    joblib.dump(node_model, 'node_cat_model.pkl')
    print("\nNode Categorization Results:")
    node_predictions_df = pd.DataFrame(node_predictions, columns=["Category"])
    print(node_predictions_df.head())

    # === Anomaly Detection (data.txt) ===
    anomaly_data, anomaly_model = detect_anomalies(analyzed_data)
    visualize_anomalies(anomaly_data)
    joblib.dump(anomaly_model, "anomaly_detection_model.pkl")

    print("✅ All models trained and saved successfully!")
