from django.contrib import admin
from .models import Game, GameConfiguration

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'provider', 'is_active')
    list_filter = ('provider', 'is_active')

@admin.register(GameConfiguration)
class GameConfigurationAdmin(admin.ModelAdmin):
    list_display = ('game', 'launch_timeout_seconds')
