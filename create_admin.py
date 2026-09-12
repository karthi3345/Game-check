import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User

try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superuser created successfully!')
    else:
        # Reset password just in case
        u = User.objects.get(username='admin')
        u.set_password('admin123')
        u.save()
        print('Superuser password reset successfully!')
except Exception as e:
    print(f"Error: {e}")
