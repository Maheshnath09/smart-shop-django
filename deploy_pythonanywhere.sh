#!/bin/bash
# =============================================================
# PythonAnywhere Deployment Script for My Store
# =============================================================
# Run these commands in PythonAnywhere Bash console after cloning
# the repository. Replace 'yourusername' with your PA username.
# =============================================================

echo "=== My Store PythonAnywhere Deployment ==="
echo ""

# Step 1: Clone the repository (run this first time only)
echo "Step 1: Clone repository (skip if already done)"
echo "git clone https://github.com/Maheshnath09/smart-shop-django.git my_store"
echo ""

# Step 2: Navigate to project
echo "Step 2: Navigate to project"
echo "cd ~/my_store"
echo ""

# Step 3: Create virtual environment
echo "Step 3: Create virtual environment"
echo "mkvirtualenv --python=/usr/bin/python3.11 my_store_env"
echo ""

# Step 4: Activate virtual environment
echo "Step 4: Activate virtual environment"
echo "workon my_store_env"
echo ""

# Step 5: Install dependencies
echo "Step 5: Install dependencies"
echo "pip install -r requirements.txt"
echo "pip install whitenoise python-dotenv mysqlclient"
echo ""

# Step 6: Create .env file
echo "Step 6: Create .env file"
cat << 'EOF'
Create a .env file with:
---
SECRET_KEY=your-very-long-secret-key-here-make-it-random
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
SECURE_SSL_REDIRECT=True
---
EOF
echo ""

# Step 7: Run migrations
echo "Step 7: Run database migrations"
echo "python manage.py migrate"
echo ""

# Step 8: Collect static files
echo "Step 8: Collect static files"
echo "python manage.py collectstatic --noinput"
echo ""

# Step 9: Create superuser (optional)
echo "Step 9: Create superuser (optional)"
echo "python manage.py createsuperuser"
echo ""

echo "=== Deployment commands complete! ==="
echo ""
echo "Next steps in PythonAnywhere Web tab:"
echo "1. Create a new web app (Manual configuration, Python 3.11)"
echo "2. Set Source code: /home/yourusername/my_store"
echo "3. Set Virtualenv: /home/yourusername/.virtualenvs/my_store_env"
echo "4. Edit WSGI file - copy content from wsgi_pythonanywhere.py"
echo "5. Add static file mapping: /static/ -> /home/yourusername/my_store/staticfiles"
echo "6. Add static file mapping: /media/ -> /home/yourusername/my_store/media"
echo "7. Click Reload!"
