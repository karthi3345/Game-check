from django.db import models
from providers.models import Provider

class Game(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='games')
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    game_url = models.URLField(blank=True, null=True, help_text="Direct URL to the game if available")
    launch_url = models.URLField(blank=True, null=True, help_text="URL to trigger the game launch (e.g. from lobby)")
    expected_text = models.CharField(max_length=255, blank=True, help_text="Primary expected text to match in OCR")
    expected_text_list = models.JSONField(default=list, blank=True, help_text="List of alternate expected texts")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class GameConfiguration(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='configuration')
    launch_timeout_seconds = models.IntegerField(default=30)
    screenshot_delay_seconds = models.IntegerField(default=5)
    max_loading_seconds = models.IntegerField(default=60)
    expected_text = models.CharField(max_length=255, blank=True)
    expected_error_texts = models.JSONField(default=list, blank=True, help_text="List of error texts to fail on")
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Config for {self.game.name}"
