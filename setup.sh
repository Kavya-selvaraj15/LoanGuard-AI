#!/bin/bash
# ============================================================
# LoanGuard AI – Full Setup Script
# Run: bash setup.sh
# ============================================================

set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ██╗      ██████╗  █████╗ ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ "
echo "  ██║     ██╔═══██╗██╔══██╗████╗  ██║██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗"
echo "  ██║     ██║   ██║███████║██╔██╗ ██║██║  ███╗██║   ██║███████║██████╔╝██║  ██║"
echo "  ██║     ██║   ██║██╔══██║██║╚██╗██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║"
echo "  ███████╗╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝"
echo "  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ "
echo -e "${NC}"
echo -e "${YELLOW}  AI-Powered Fake Loan App Detection System${NC}"
echo ""

# Step 1 – Virtual environment
echo -e "${CYAN}[1/6] Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Step 2 – Install dependencies
echo -e "${CYAN}[2/6] Installing dependencies...${NC}"
pip install -r requirements.txt -q

# Step 3 – Migrations
echo -e "${CYAN}[3/6] Running database migrations...${NC}"
python manage.py makemigrations accounts apk_analysis nlp_analysis community analytics
python manage.py migrate

# Step 4 – Train AI model
echo -e "${CYAN}[4/6] Training AI fraud detection model...${NC}"
python ai_detection/train_model.py

# Step 5 – Create superuser
echo -e "${CYAN}[5/6] Creating default admin user...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@loanguard.com', 'admin123')
    print('Admin created: username=admin  password=admin123')
else:
    print('Admin already exists.')
"

# Step 6 – Collect static
echo -e "${CYAN}[6/6] Collecting static files...${NC}"
python manage.py collectstatic --noinput -v 0

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✅  LoanGuard AI is ready!             ║${NC}"
echo -e "${GREEN}╠══════════════════════════════════════════╣${NC}"
echo -e "${GREEN}║  Run:  python manage.py runserver        ║${NC}"
echo -e "${GREEN}║  URL:  http://127.0.0.1:8000             ║${NC}"
echo -e "${GREEN}║  Admin: http://127.0.0.1:8000/admin/     ║${NC}"
echo -e "${GREEN}║  User:  admin  │  Pass: admin123         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════╝${NC}"
echo ""
read -p "Start server now? [y/N] " yn
if [[ "$yn" =~ ^[Yy]$ ]]; then
    python manage.py runserver
fi
