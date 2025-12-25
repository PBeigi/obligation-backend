"""
Script to recreate Google OAuth SocialApp configuration
Run with: python manage.py shell < setup_google_oauth.py
"""
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import json

# Load client secret
with open('client_secret.json') as f:
    config = json.load(f)
    client_id = config['web']['client_id']
    client_secret = config['web']['client_secret']

# Get or create the SocialApp
app, created = SocialApp.objects.get_or_create(
    provider='google',
    defaults={
        'name': 'Google',
        'client_id': client_id,
        'secret': client_secret,
    }
)

if not created:
    app.client_id = client_id
    app.secret = client_secret
    app.save()
    print("Updated existing Google SocialApp")
else:
    print("Created new Google SocialApp")

# Add site
site = Site.objects.get(id=1)
if site not in app.sites.all():
    app.sites.add(site)
    print(f"Added site: {site.domain}")

print(f"Google OAuth configured successfully!")
print(f"Client ID: {client_id[:20]}...")
