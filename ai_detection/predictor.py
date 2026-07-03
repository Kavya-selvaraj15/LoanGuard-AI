"""
AI Fraud Detection Predictor
Uses RandomForest trained on permission features to classify loan apps.
Falls back to rule-based scoring if model not trained yet.
"""
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

# High-risk permissions that strongly indicate fraud
HIGH_RISK_INDICATORS = {
    'READ_SMS': 20,
    'RECEIVE_SMS': 18,
    'READ_CONTACTS': 18,
    'ACCESS_FINE_LOCATION': 15,
    'RECORD_AUDIO': 15,
    'READ_CALL_LOG': 15,
    'WRITE_CONTACTS': 12,
    'PROCESS_OUTGOING_CALLS': 12,
    'SEND_SMS': 10,
    'CAMERA': 8,
    'READ_EXTERNAL_STORAGE': 6,
    'WRITE_EXTERNAL_STORAGE': 6,
    'READ_PHONE_STATE': 5,
    'RECEIVE_BOOT_COMPLETED': 4,
    'GET_ACCOUNTS': 4,
    'CHANGE_NETWORK_STATE': 3,
}


def _build_feature_vector(permissions):
    """Create a feature vector from permission list."""
    perm_names = {p['name'].upper() for p in permissions}
    features = {
        'has_read_sms': int('READ_SMS' in perm_names),
        'has_read_contacts': int('READ_CONTACTS' in perm_names),
        'has_location': int('ACCESS_FINE_LOCATION' in perm_names or
                            'ACCESS_COARSE_LOCATION' in perm_names),
        'has_camera': int('CAMERA' in perm_names),
        'has_record_audio': int('RECORD_AUDIO' in perm_names),
        'has_read_call_log': int('READ_CALL_LOG' in perm_names),
        'has_read_storage': int('READ_EXTERNAL_STORAGE' in perm_names),
        'has_write_storage': int('WRITE_EXTERNAL_STORAGE' in perm_names),
        'has_receive_boot': int('RECEIVE_BOOT_COMPLETED' in perm_names),
        'has_get_accounts': int('GET_ACCOUNTS' in perm_names),
        'total_permissions': len(permissions),
        'high_risk_count': sum(1 for p in permissions if p.get('risk_level') == 'high'),
        'medium_risk_count': sum(1 for p in permissions if p.get('risk_level') == 'medium'),
    }
    return np.array(list(features.values())).reshape(1, -1)


def _rule_based_score(permissions):
    """Fallback rule-based fraud scoring (0-100)."""
    perm_names = {p['name'].upper() for p in permissions}
    score = 0
    for perm, weight in HIGH_RISK_INDICATORS.items():
        if perm in perm_names:
            score += weight
    return min(score, 100)


def predict_fraud(permissions):
    """
    Main prediction function.
    Returns dict with fraud_probability (0-100) and risk_level.
    """
    # Try ML model first
    try:
        import joblib
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            X = _build_feature_vector(permissions)
            prob = model.predict_proba(X)[0][1] * 100
        else:
            raise FileNotFoundError("Model not trained yet")
    except Exception:
        # Rule-based fallback
        prob = _rule_based_score(permissions)

    prob = round(prob, 2)

    if prob >= 65:
        risk_level = 'Dangerous'
        recommendation = (
            'HIGH RISK: This app shows strong indicators of fraud. '
            'It requests dangerous permissions typically used for harassment, '
            'data theft, and financial fraud. DO NOT INSTALL.'
        )
        color = 'danger'
    elif prob >= 35:
        risk_level = 'Medium Risk'
        recommendation = (
            'MODERATE RISK: This app has some suspicious permissions. '
            'Install only if you fully trust the source. '
            'Be cautious about granting all requested permissions.'
        )
        color = 'warning'
    else:
        risk_level = 'Safe'
        recommendation = (
            'LOW RISK: This app appears relatively safe. '
            'No major dangerous permissions detected. '
            'Always read terms before borrowing.'
        )
        color = 'success'

    return {
        'fraud_probability': prob,
        'risk_level': risk_level,
        'recommendation': recommendation,
        'color': color,
    }
