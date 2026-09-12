from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('QA', 'QA'),
        ('VIEWER', 'Viewer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='VIEWER')

class EnvironmentConfiguration(models.fields.Model if hasattr(models.fields, 'Model') else models.Model):
    name = models.CharField(max_length=100)
    base_url = models.URLField()
    login_credentials_env_key = models.CharField(max_length=100, help_text="The environment variable key storing the login credentials (e.g. MYVEPOWER_CREDENTIALS)")
    game_lobby_url = models.URLField(blank=True, null=True)
    browser = models.CharField(max_length=50, default="Chromium")
    headless = models.BooleanField(default=True)
    launch_timeout_seconds = models.IntegerField(default=30)
    enable_screenshot = models.BooleanField(default=True)
    enable_ocr = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.base_url})"
