from django.db import models
from core.models import EnvironmentConfiguration
from providers.models import Provider
from games.models import Game

class TestRun(models.Model):
    TRIGGER_CHOICES = [
        ('MANUAL', 'Manual'),
        ('SCHEDULED', 'Scheduled'),
        ('BULK', 'Bulk'),
    ]
    STATUS_CHOICES = [
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('PARTIAL', 'Partial'),
        ('FAILED', 'Failed'),
    ]
    
    environment = models.ForeignKey(EnvironmentConfiguration, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    triggered_by = models.CharField(max_length=100)
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RUNNING')

    def __str__(self):
        return f"Run #{self.id} ({self.status})"

class GameTestResult(models.Model):
    FINAL_STATUS_CHOICES = [
        ('PASS', 'Pass'),
        ('FAIL', 'Fail'),
        ('WARNING', 'Warning'),
        ('NOT_TESTED', 'Not Tested'),
    ]

    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name='results')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='test_results')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Individual checks
    url_check_status = models.CharField(max_length=20, default='NOT_TESTED')
    http_status_code = models.IntegerField(null=True, blank=True)
    page_load_status = models.CharField(max_length=20, default='NOT_TESTED')
    launch_status = models.CharField(max_length=20, default='NOT_TESTED')
    game_screen_status = models.CharField(max_length=20, default='NOT_TESTED')
    loading_status = models.CharField(max_length=20, default='NOT_TESTED')
    console_status = models.CharField(max_length=20, default='NOT_TESTED')
    network_status = models.CharField(max_length=20, default='NOT_TESTED')
    ocr_status = models.CharField(max_length=20, default='NOT_TESTED')
    expected_text_status = models.CharField(max_length=20, default='NOT_TESTED')

    # Metrics
    page_load_time_ms = models.IntegerField(null=True, blank=True)
    launch_time_ms = models.IntegerField(null=True, blank=True)
    screenshot_time_ms = models.IntegerField(null=True, blank=True)

    # Evidence
    screenshot_url = models.URLField(blank=True, null=True)
    screenshot_path = models.CharField(max_length=500, blank=True, null=True)
    ocr_text = models.TextField(blank=True, null=True)
    console_errors = models.JSONField(default=list, blank=True)
    network_errors = models.JSONField(default=list, blank=True)
    error_message = models.TextField(blank=True, null=True)

    # Final
    final_status = models.CharField(max_length=20, choices=FINAL_STATUS_CHOICES, default='NOT_TESTED')
    failure_reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.game.name} - {self.final_status}"
