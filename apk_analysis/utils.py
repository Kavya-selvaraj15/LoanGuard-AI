"""
APK Analysis Utility
Extracts permissions and analyzes risk without requiring Androguard (fallback included).
"""

import os
import zipfile
import re

# Dangerous permissions with descriptions and risk levels
DANGEROUS_PERMISSIONS = {
    'READ_SMS': {
        'level': 'high',
        'description': 'Reads all SMS messages — can steal OTPs and banking messages'
    },
    'RECEIVE_SMS': {
        'level': 'high',
        'description': 'Intercepts incoming SMS — can silently monitor messages'
    },
    'SEND_SMS': {
        'level': 'high',
        'description': 'Sends SMS without user consent — potential for spam or fraud'
    },
    'READ_CONTACTS': {
        'level': 'high',
        'description': 'Access to all contacts — used for harassment in fake loan apps'
    },
    'WRITE_CONTACTS': {
        'level': 'high',
        'description': 'Modify contacts — can inject fake entries'
    },
    'ACCESS_FINE_LOCATION': {
        'level': 'high',
        'description': 'Precise GPS location tracking — serious privacy violation'
    },
    'ACCESS_COARSE_LOCATION': {
        'level': 'medium',
        'description': 'Approximate location — can track general whereabouts'
    },
    'CAMERA': {
        'level': 'medium',
        'description': 'Camera access — can capture photos silently'
    },
    'RECORD_AUDIO': {
        'level': 'high',
        'description': 'Microphone access — can record calls and surroundings'
    },
    'READ_CALL_LOG': {
        'level': 'high',
        'description': 'Access to call history — severe privacy invasion'
    },
    'WRITE_CALL_LOG': {
        'level': 'high',
        'description': 'Modify call logs — can falsify records'
    },
    'READ_EXTERNAL_STORAGE': {
        'level': 'medium',
        'description': 'Read files from storage — can access personal documents'
    },
    'WRITE_EXTERNAL_STORAGE': {
        'level': 'medium',
        'description': 'Write to storage — can drop malicious files'
    },
    'PROCESS_OUTGOING_CALLS': {
        'level': 'high',
        'description': 'Monitor and redirect outgoing calls'
    },
    'GET_ACCOUNTS': {
        'level': 'medium',
        'description': 'Access linked Google/social accounts'
    },
    'USE_BIOMETRIC': {
        'level': 'medium',
        'description': 'Fingerprint/face ID access'
    },
    'READ_PHONE_STATE': {
        'level': 'medium',
        'description': 'Read phone identity (IMEI, SIM) — used for device fingerprinting'
    },
    'INTERNET': {
        'level': 'low',
        'description': 'Basic internet access — required for all apps'
    },
    'VIBRATE': {
        'level': 'low',
        'description': 'Controls vibration — harmless'
    },
    'RECEIVE_BOOT_COMPLETED': {
        'level': 'medium',
        'description': 'Starts automatically on device boot — can run in background'
    },
    'FOREGROUND_SERVICE': {
        'level': 'low',
        'description': 'Runs visible foreground service'
    },
    'WAKE_LOCK': {
        'level': 'low',
        'description': 'Keeps device awake — can drain battery'
    },
    'CHANGE_NETWORK_STATE': {
        'level': 'medium',
        'description': 'Can modify network connectivity'
    },
    'ACCESS_WIFI_STATE': {
        'level': 'low',
        'description': 'Read Wi-Fi connection info'
    },
}


def extract_permissions_from_apk(apk_path):
    """
    Try Androguard first; fall back to raw zip/manifest parsing.
    Returns (permissions_list, package_name, app_name)
    """
    try:
        from androguard.core.bytecodes.apk import APK
        apk = APK(apk_path)
        raw_perms = apk.get_permissions()
        package = apk.get_package() or 'unknown.package'
        app_name = apk.get_app_name() or os.path.basename(apk_path)
        return _process_permissions(raw_perms), package, app_name
    except Exception:
        pass

    # Fallback: parse AndroidManifest.xml from zip
    try:
        return _fallback_parse(apk_path)
    except Exception:
        return [], 'unknown.package', os.path.basename(apk_path)


def _fallback_parse(apk_path):
    """Parse permissions from raw zip manifest."""
    permissions = []
    package = 'unknown.package'
    app_name = os.path.basename(apk_path)
    try:
        with zipfile.ZipFile(apk_path, 'r') as z:
            if 'AndroidManifest.xml' in z.namelist():
                raw = z.read('AndroidManifest.xml')
                # Extract permission strings from binary XML
                text = raw.decode('latin-1', errors='ignore')
                found = re.findall(r'android\.permission\.([A-Z_]+)', text)
                permissions = _process_permissions(
                    [f'android.permission.{p}' for p in found]
                )
                pkg_match = re.search(r'package["\s=]+"?([a-z][a-zA-Z0-9_.]+)', text)
                if pkg_match:
                    package = pkg_match.group(1)
    except Exception:
        pass
    return permissions, package, app_name


def _process_permissions(raw_perms):
    """Convert raw permission strings into structured dicts."""
    seen = set()
    result = []
    for p in raw_perms:
        name = p.split('.')[-1].upper()
        if name in seen:
            continue
        seen.add(name)
        info = DANGEROUS_PERMISSIONS.get(name, {
            'level': 'low',
            'description': f'Permission: {name}'
        })
        result.append({
            'name': name,
            'full_name': p,
            'risk_level': info['level'],
            'description': info['description'],
        })
    return result


def calculate_permission_risk_score(permissions):
    """Score 0–100 based on dangerous permissions found."""
    weights = {'high': 15, 'medium': 7, 'low': 1}
    score = sum(weights.get(p['risk_level'], 0) for p in permissions)
    return min(score, 100)


def simulate_apk_scan(app_name):
    """
    Demo scanner for testing without a real APK.
    Simulates a dangerous loan app.
    """
    import random
    dangerous_set = [
        'READ_SMS', 'READ_CONTACTS', 'ACCESS_FINE_LOCATION',
        'CAMERA', 'RECORD_AUDIO', 'READ_CALL_LOG',
    ]
    safe_set = ['INTERNET', 'VIBRATE', 'WAKE_LOCK', 'ACCESS_WIFI_STATE']
    chosen_dangerous = random.sample(dangerous_set, k=random.randint(2, 5))
    chosen_safe = random.sample(safe_set, k=random.randint(1, 3))
    all_chosen = chosen_dangerous + chosen_safe
    permissions = _process_permissions([f'android.permission.{p}' for p in all_chosen])
    return permissions, f'com.fake.{app_name.lower().replace(" ", "")}', app_name
