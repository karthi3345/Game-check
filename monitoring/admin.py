from django.contrib import admin
from .models import TestRun, GameTestResult

@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'trigger_type', 'started_at', 'completed_at')
    list_filter = ('status', 'trigger_type')

@admin.register(GameTestResult)
class GameTestResultAdmin(admin.ModelAdmin):
    list_display = ('game', 'provider', 'test_run', 'final_status', 'completed_at')
    list_filter = ('final_status', 'provider')
