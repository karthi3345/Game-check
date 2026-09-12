import yaml
from django.core.management.base import BaseCommand
from providers.models import Provider
from games.models import Game, GameConfiguration

class Command(BaseCommand):
    help = 'Imports games and providers from a YAML file'

    def add_arguments(self, parser):
        parser.add_argument('yaml_file', type=str, help='Path to the YAML file')

    def handle(self, *args, **options):
        yaml_file = options['yaml_file']
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            providers_data = data.get('providers', [])
            
            for provider_data in providers_data:
                provider_code = provider_data.get('code')
                if not provider_code:
                    continue
                    
                provider, created = Provider.objects.get_or_create(
                    code=provider_code,
                    defaults={
                        'name': provider_data.get('name', provider_code),
                        'base_url': provider_data.get('base_url', ''),
                    }
                )
                
                games_data = provider_data.get('games', [])
                for game_data in games_data:
                    identifier = game_data.get('identifier')
                    if not identifier:
                        continue
                        
                    game, g_created = Game.objects.update_or_create(
                        identifier=identifier,
                        defaults={
                            'provider': provider,
                            'name': game_data.get('name', identifier),
                            'category': game_data.get('category', ''),
                            'game_url': game_data.get('game_url', ''),
                            'launch_url': game_data.get('launch_url', ''),
                            'expected_text': game_data.get('expected_text', ''),
                        }
                    )
                    
                    config_data = game_data.get('config', {})
                    if config_data:
                        GameConfiguration.objects.update_or_create(
                            game=game,
                            defaults={
                                'launch_timeout_seconds': config_data.get('launch_timeout_seconds', 30),
                                'expected_error_texts': config_data.get('expected_error_texts', []),
                            }
                        )
                        
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(providers_data)} providers.'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing YAML: {e}'))
