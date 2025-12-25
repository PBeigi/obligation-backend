"""
Quick test script to create sample obligations
Run with: python manage.py shell < test_data.py
"""
from django.utils import timezone
from datetime import timedelta
from users.models import User
from obligations.models import Obligation

# Get or create two test users (you'll need to create these via Google OAuth first)
try:
    user1 = User.objects.get(email='your-email@gmail.com')  # Replace with your Google email
    print(f"Found user: {user1.email}")
    
    # Create a test obligation where you owe someone
    obligation = Obligation.objects.create(
        title="Buy coffee for the team",
        description="Promised to bring coffee on Friday",
        owed_by=user1,  # You owe
        owed_to=user1,  # To yourself (for testing, though validation prevents this in API)
        due_at=timezone.now() + timedelta(days=2),
        status='PENDING'
    )
    print(f"Created obligation: {obligation}")
    
except User.DoesNotExist:
    print("No users found. Please log in via Google OAuth first at /accounts/google/login/")
