"""
Train the LoanGuard fraud detection model.
Run: python manage.py shell < ai_detection/train_model.py
OR: python ai_detection/train_model.py
"""
import numpy as np
import os

def train_and_save():
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, classification_report
        import joblib
    except ImportError:
        print("Install scikit-learn: pip install scikit-learn joblib")
        return

    # Generate synthetic training data
    # Features: read_sms, read_contacts, location, camera, record_audio,
    #           read_call_log, read_storage, write_storage, receive_boot,
    #           get_accounts, total_perms, high_risk_count, medium_risk_count
    np.random.seed(42)

    # Fraud apps (label=1) — high dangerous permissions
    fraud_data = []
    for _ in range(300):
        row = [
            np.random.choice([0, 1], p=[0.2, 0.8]),  # read_sms
            np.random.choice([0, 1], p=[0.15, 0.85]),  # read_contacts
            np.random.choice([0, 1], p=[0.3, 0.7]),   # location
            np.random.choice([0, 1], p=[0.4, 0.6]),   # camera
            np.random.choice([0, 1], p=[0.5, 0.5]),   # record_audio
            np.random.choice([0, 1], p=[0.4, 0.6]),   # read_call_log
            np.random.choice([0, 1], p=[0.3, 0.7]),   # read_storage
            np.random.choice([0, 1], p=[0.4, 0.6]),   # write_storage
            np.random.choice([0, 1], p=[0.5, 0.5]),   # receive_boot
            np.random.choice([0, 1], p=[0.5, 0.5]),   # get_accounts
        ]
        total = sum(row) + np.random.randint(5, 15)
        high = sum(row[:6])
        medium = sum(row[6:]) + np.random.randint(0, 3)
        row.extend([total, high, medium])
        fraud_data.append(row + [1])

    # Safe apps (label=0) — low dangerous permissions
    safe_data = []
    for _ in range(300):
        row = [
            np.random.choice([0, 1], p=[0.95, 0.05]),  # read_sms
            np.random.choice([0, 1], p=[0.9, 0.1]),   # read_contacts
            np.random.choice([0, 1], p=[0.85, 0.15]),  # location
            np.random.choice([0, 1], p=[0.7, 0.3]),   # camera
            np.random.choice([0, 1], p=[0.9, 0.1]),   # record_audio
            np.random.choice([0, 1], p=[0.95, 0.05]),  # read_call_log
            np.random.choice([0, 1], p=[0.6, 0.4]),   # read_storage
            np.random.choice([0, 1], p=[0.7, 0.3]),   # write_storage
            np.random.choice([0, 1], p=[0.8, 0.2]),   # receive_boot
            np.random.choice([0, 1], p=[0.7, 0.3]),   # get_accounts
        ]
        total = sum(row) + np.random.randint(1, 6)
        high = sum(row[:6])
        medium = sum(row[6:])
        row.extend([total, high, medium])
        safe_data.append(row + [0])

    all_data = np.array(fraud_data + safe_data)
    X = all_data[:, :-1]
    y = all_data[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc * 100:.1f}%")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Fraud']))

    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    return acc


if __name__ == '__main__':
    train_and_save()
