from rest_framework import serializers
from .models import Game, GameConfiguration

class GameConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameConfiguration
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    configuration = GameConfigurationSerializer(read_only=True)

    class Meta:
        model = Game
        fields = '__all__'
