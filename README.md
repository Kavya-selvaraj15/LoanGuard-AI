# 🛡️ LoanGuard AI – Fake Loan App Detection System

An AI-powered cybersecurity platform that identifies fraudulent loan applications by analyzing APK permissions, user reviews, and app risk indicators.

---

## 📁 Complete Project Structure

```
loanguard/                          ← Root project folder
│
├── manage.py                       ← Django entry point
├── requirements.txt                ← Python dependencies
├── setup.sh                        ← One-click setup script
├── db.sqlite3                      ← SQLite database (auto-created)
│
├── loanguard/                      ← Django project config
│   ├── __init__.py
│   ├── settings.py                 ← All settings (DB, apps, JWT, media)
│   ├── urls.py                     ← Root URL router
│   └── wsgi.py                     ← WSGI for deployment
│
├── accounts/                       ← Authentication module
│   ├── models.py                   ← CustomUser model
│   ├── views.py                    ← Login, Register, Logout, Profile
│   ├── forms.py                    ← RegisterForm, LoginForm
│   ├── urls.py                     ← Web URLs (/accounts/login/ etc.)
│   ├── api_urls.py                 ← REST API URLs
│   ├── api_views.py                ← JWT login, register API
│   └── admin.py                    ← Admin panel config
│
├── apk_analysis/                   ← APK upload & analysis module
│   ├── models.py                   ← LoanApp, Permission models
│   ├── views.py                    ← Upload, Result, History, Dashboard
│   ├── utils.py                    ← Androguard + permission parser
│   ├── urls.py                     ← Web URLs (/apk/upload/ etc.)
│   ├── api_urls.py                 ← REST API URLs
│   ├── api_views.py                ← Upload & result APIs
│   └── admin.py
│
├── ai_detection/                   ← AI / ML fraud detection
│   ├── predictor.py                ← Fraud prediction logic (ML + rule-based)
│   ├── train_model.py              ← Model training script
│   ├── model.pkl                   ← Trained RandomForest model (auto-generated)
│   ├── models.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── train_model.py      ← Django management command
│
├── nlp_analysis/                   ← NLP review analysis module
│   ├── models.py                   ← Review model
│   ├── analyzer.py                 ← TextBlob + keyword detection
│   ├── views.py
│   └── urls.py
│
├── community/                      ← Community scam reports
│   ├── models.py                   ← ScamReport model
│   ├── views.py                    ← Submit, list reports
│   ├── forms.py                    ← ScamReportForm
│   ├── urls.py
│   ├── api_urls.py
│   ├── api_views.py
│   └── admin.py
│
├── analytics/                      ← Analytics & statistics
│   ├── models.py                   ← AnalyticsSummary model
│   ├── views.py                    ← Analytics dashboard
│   ├── urls.py
│   ├── api_urls.py
│   └── api_views.py
│
├── templates/                      ← All HTML templates
│   ├── base.html                   ← Master layout (sidebar, topbar, nav)
│   ├── accounts/
│   │   ├── login.html              ← Login page
│   │   ├── register.html           ← Registration page
│   │   └── profile.html            ← User profile
│   ├── apk_analysis/
│   │   ├── dashboard.html          ← Main dashboard with charts
│   │   ├── upload.html             ← APK upload page
│   │   ├── result.html             ← Full fraud analysis report
│   │   └── history.html            ← Scan history with filters
│   ├── community/
│   │   ├── reports.html            ← Community reports list
│   │   └── submit_report.html      ← Report submission form
│   ├── analytics/
│   │   └── analytics.html          ← Analytics with Chart.js
│   └── nlp_analysis/
│       └── reviews.html            ← Standalone NLP analyzer
│
├── static/                         ← Static files
│   ├── css/
│   │   └── main.css                ← Extra styles & animations
│   └── js/
│       └── main.js                 ← API helper, toast, utilities
│
└── media/                          ← User uploads
    ├── apks/                       ← Uploaded APK files
    └── screenshots/                ← Report screenshots
```

---

## ⚙️ Installation & Setup

### Method 1 – Automatic (Recommended)
```bash
git clone <your-repo-url>
cd loanguard
bash setup.sh
```

### Method 2 – Manual Step by Step

**Step 1: Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run migrations**
```bash
python manage.py makemigrations accounts apk_analysis nlp_analysis community analytics
python manage.py migrate
```

**Step 4: Train AI model**
```bash
python ai_detection/train_model.py
```

**Step 5: Create admin user**
```bash
python manage.py createsuperuser
# OR use default: username=admin, password=admin123
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin','admin@loanguard.com','admin123')
"
```

**Step 6: Start the server**
```bash
python manage.py runserver
```

**Step 7: Open in browser**
```
http://127.0.0.1:8000/accounts/login/
http://127.0.0.1:8000/admin/
```

---

## 🌐 All Application URLs

| URL | Page | Auth |
|-----|------|------|
| `/accounts/login/` | Login | Public |
| `/accounts/register/` | Register | Public |
| `/accounts/logout/` | Logout | Login required |
| `/accounts/profile/` | User profile | Login required |
| `/apk/dashboard/` | Main dashboard | Login required |
| `/apk/upload/` | Scan APK / app | Login required |
| `/apk/result/<id>/` | Scan result | Login required |
| `/apk/history/` | Scan history | Login required |
| `/community/reports/` | Scam reports | Login required |
| `/community/submit/` | Submit report | Login required |
| `/analytics/` | Analytics charts | Login required |
| `/nlp/reviews/` | Review analyzer | Login required |
| `/admin/` | Django admin | Admin only |

## 🔌 REST API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/accounts/register/` | Register user |
| POST | `/api/accounts/token/` | Get JWT token (login) |
| POST | `/api/accounts/token/refresh/` | Refresh JWT |
| GET  | `/api/accounts/profile/` | Get user profile |
| POST | `/api/apk/upload/` | Upload & analyze APK |
| GET  | `/api/apk/result/<id>/` | Get scan result |
| GET  | `/api/apk/history/` | Get scan history |
| GET  | `/api/community/reports/` | List scam reports |
| POST | `/api/community/submit/` | Submit scam report |
| GET  | `/api/analytics/summary/` | Get analytics data |

---

## 🗄️ Database Tables

| Table | Key Fields |
|-------|-----------|
| `accounts_customuser` | id, username, email, password, phone, created_at |
| `apk_analysis_loanapp` | id, app_name, package_name, risk_score, risk_level, fraud_probability |
| `apk_analysis_permission` | id, app_id, permission_name, risk_level, description |
| `nlp_analysis_review` | id, app_id, review_text, sentiment, polarity, is_scam_review |
| `community_scamreport` | id, user_id, app_name, description, screenshot, status |
| `analytics_analyticssummary` | id, date, total_scans, dangerous_apps, safe_apps |

---

## 🧠 How the AI Works

```
APK File → Androguard Parser → Permission List
                                      ↓
              Feature Vector: [has_read_sms, has_contacts, has_location,
                               has_camera, has_record_audio, has_call_log,
                               has_storage, has_boot, total_perms,
                               high_risk_count, medium_risk_count]
                                      ↓
                         RandomForest Classifier (200 trees)
                                      ↓
                         Fraud Probability: 0–100%
                                      ↓
               Safe (0–34%) | Medium Risk (35–64%) | Dangerous (65–100%)
```

---

## 🔒 Security Features

- **Password hashing** – Django's bcrypt/PBKDF2
- **JWT Authentication** – Access + refresh tokens
- **CSRF protection** – Django middleware
- **Input validation** – Forms + serializers
- **File type verification** – APK upload validation
- **Session management** – Secure session handling
- **SQL injection prevention** – Django ORM (parameterized queries)

---

## 🚀 Deployment (Production)

```bash
# Install production server
pip install gunicorn whitenoise

# Update settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Collect static files
python manage.py collectstatic

# Start with Gunicorn
gunicorn loanguard.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

**Nginx config (`/etc/nginx/sites-available/loanguard`):**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    location / { proxy_pass http://127.0.0.1:8000; }
    location /media/ { alias /path/to/loanguard/media/; }
    location /static/ { alias /path/to/loanguard/staticfiles/; }
}
```

---

## 🧪 Running Tests

```bash
python manage.py test accounts apk_analysis community
```

---

## 📞 Default Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |

> ⚠️ Change the admin password immediately in production!
