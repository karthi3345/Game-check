from django.shortcuts import render
from monitoring.models import GameTestResult, TestRun
from games.models import Game
from providers.models import Provider

def dashboard_home(request):
    latest_results = GameTestResult.objects.select_related('game', 'provider').order_by('-completed_at')[:20]
    total_games = Game.objects.count()
    active_providers = Provider.objects.filter(is_active=True).count()
    failed_tests = GameTestResult.objects.filter(final_status='FAIL').count()
    
    context = {
        'latest_results': latest_results,
        'total_games': total_games,
        'active_providers': active_providers,
        'failed_tests': failed_tests,
    }
    return render(request, 'dashboard/home.html', context)

def provider_list(request):
    providers = Provider.objects.all()
    return render(request, 'dashboard/provider_list.html', {'providers': providers})

def provider_detail(request, pk):
    provider = Provider.objects.get(pk=pk)
    games = provider.games.all()
    return render(request, 'dashboard/provider_detail.html', {'provider': provider, 'games': games})

def test_history(request):
    results = GameTestResult.objects.select_related('game', 'provider').order_by('-completed_at')[:100]
    return render(request, 'dashboard/test_history.html', {'results': results})
