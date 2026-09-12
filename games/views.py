from rest_framework import viewsets
from .models import Game, GameConfiguration
from .serializers import GameSerializer, GameConfigurationSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameConfigurationViewSet(viewsets.ModelViewSet):
    queryset = GameConfiguration.objects.all()
    serializer_class = GameConfigurationSerializer
