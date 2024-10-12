#!/bin/bash

# Activate virtual environment
source /var/www/polycoid/.venv/bin/activate

# Navigate to the project directory
cd /var/www/polycoid

eval "$(ssh-agent -s)"  # Start the SSH agent
ssh-add ~/.ssh/github   

# Pull the latest changes from GitHub
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart Gunicorn
sudo systemctl restart gunicorn

# Restart Nginx (optional)
sudo systemctl restart nginx
