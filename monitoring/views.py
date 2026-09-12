from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import TestRun, GameTestResult
from .tasks import run_bulk_test, run_game_test

class MonitoringViewSet(viewsets.ViewSet):
    """
    API endpoint that allows monitoring tasks to be triggered.
    """
    
    @action(detail=False, methods=['post'])
    def trigger_bulk(self, request):
        provider_id = request.data.get('provider_id')
        task = run_bulk_test.delay(provider_id=provider_id)
        return Response({'task_id': task.id, 'status': 'Bulk test initiated'}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['post'])
    def trigger_game(self, request, pk=None):
        # Create a dummy test run
        test_run = TestRun.objects.create(trigger_type='MANUAL')
        task = run_game_test.delay(test_run.id, pk)
        return Response({'task_id': task.id, 'status': f'Game {pk} test initiated'}, status=status.HTTP_202_ACCEPTED)
