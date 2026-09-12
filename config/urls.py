from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from providers.views import ProviderViewSet
from games.views import GameViewSet, GameConfigurationViewSet
from monitoring.views import MonitoringViewSet

router = DefaultRouter()
router.register(r'providers', ProviderViewSet)
router.register(r'games', GameViewSet)
router.register(r'game-configurations', GameConfigurationViewSet)
router.register(r'monitoring', MonitoringViewSet, basename='monitoring')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('dashboard.urls')),
]
