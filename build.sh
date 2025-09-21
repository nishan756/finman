set -o errexit

# Requirements install
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput


# Apply all migrations
python manage.py migrate
python manage.py createsu
