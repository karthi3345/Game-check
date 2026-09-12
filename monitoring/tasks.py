from celery import shared_task
from django.utils import timezone
from core.models import EnvironmentConfiguration
from monitoring.models import TestRun, GameTestResult
from games.models import Game
from .services.browser_service import BrowserService
from .services.screenshot_service import ScreenshotService
from .services.ocr_service import OCRService
from .services.result_analyzer import ResultAnalyzer
from .services.alert_service import AlertService

@shared_task
def run_game_test(test_run_id: int, game_id: int):
    """Executes a health check for a single game."""
    try:
        test_run = TestRun.objects.get(id=test_run_id)
        game = Game.objects.select_related('configuration', 'provider').get(id=game_id)
        config = test_run.environment
        
        result = GameTestResult.objects.create(
            test_run=test_run,
            game=game,
            provider=game.provider,
            status='RUNNING'
        )

        browser = BrowserService(config)
        browser.start()
        
        # 1. Login
        logged_in = browser.login()
        if not logged_in:
            result.final_status = 'FAIL'
            result.failure_reason = 'AUTH_FAILED'
            result.completed_at = timezone.now()
            result.save()
            browser.close()
            return
            
        # 2. Launch Game
        target_url = game.launch_url or game.game_url
        if not target_url:
            result.final_status = 'FAIL'
            result.failure_reason = 'NO_URL_CONFIGURED'
            result.completed_at = timezone.now()
            result.save()
            browser.close()
            return

        nav_metrics = browser.navigate_to_game(target_url)
        
        # Merge metrics
        result.url_check_status = nav_metrics.get('url_check_status', 'FAIL')
        result.http_status_code = nav_metrics.get('http_status_code')
        result.page_load_status = nav_metrics.get('page_load_status', 'FAIL')
        result.page_load_time_ms = nav_metrics.get('page_load_time_ms')
        
        # We assume game screen loads if page loads for now.
        # In a real environment with the exact Myvepower CSS, this would wait for the canvas/iframe.
        result.launch_status = result.page_load_status
        result.game_screen_status = result.page_load_status
        
        # 3. Screenshot & OCR
        if result.game_screen_status == 'PASS' and config.enable_screenshot:
            screenshot_svc = ScreenshotService()
            filename = screenshot_svc.generate_filename(game.provider.code, game.slug or str(game.id), test_run.id)
            filepath = screenshot_svc.get_absolute_path(filename)
            
            # Take screenshot
            try:
                browser.page.screenshot(path=filepath)
                result.screenshot_path = filepath
                result.screenshot_url = screenshot_svc.get_url(filename)
                
                if config.enable_ocr:
                    ocr_svc = OCRService()
                    extracted = ocr_svc.extract_text(filepath)
                    result.ocr_text = extracted
                    result.ocr_status = 'PASS' if extracted else 'WARNING'
                    
                    # Expected text check
                    expected = getattr(game, 'expected_text', '')
                    if expected:
                        matched = ocr_svc.compare_expected_text(extracted, expected)
                        result.expected_text_status = 'PASS' if matched else 'FAIL'
                    
                    # Error text check
                    error_patterns = getattr(game, 'configuration', {}).expected_error_texts if hasattr(game, 'configuration') else []
                    has_error, err_msg = ocr_svc.detect_error_text(extracted, error_patterns)
                    if has_error:
                        result.error_message = f"Found error on screen: {err_msg}"
                        
            except Exception as e:
                print(f"Screenshot/OCR error: {e}")
                
        # 4. Final Status
        analyzer = ResultAnalyzer()
        
        # Build dict for analyzer
        res_dict = {
            'url_check_status': result.url_check_status,
            'page_load_status': result.page_load_status,
            'launch_status': result.launch_status,
            'game_screen_status': result.game_screen_status,
            'expected_text_status': result.expected_text_status,
            'ocr_status': result.ocr_status,
            'network_errors': [], # To be implemented via page.on('requestfailed')
            'console_errors': [], # To be implemented via page.on('console')
            'page_load_time_ms': result.page_load_time_ms,
            'launch_time_ms': result.page_load_time_ms # Same for now
        }
        
        if result.error_message:
            res_dict['ocr_status'] = 'FAIL'
            
        final_status = analyzer.calculate_final_status(res_dict)
        result.final_status = final_status
        result.completed_at = timezone.now()
        
        # Determine failure reason for alerts
        if final_status != 'PASS':
            fail_reasons = []
            for key, val in res_dict.items():
                if val == 'FAIL':
                    fail_reasons.append(key)
            result.failure_reason = " | ".join(fail_reasons) or result.error_message
            
            # Send alert
            alert_svc = AlertService()
            alert_svc.send_alert(game.name, final_status, {
                'url_check_status': result.url_check_status,
                'page_load_time_ms': result.page_load_time_ms,
                'failure_reason': result.failure_reason
            })
            
        result.save()
        
        browser.close()
        
    except Exception as e:
        print(f"Task failed: {e}")

@shared_task
def run_bulk_test(environment_id: int):
    """Triggers tests for all active games."""
    env = EnvironmentConfiguration.objects.get(id=environment_id)
    
    test_run = TestRun.objects.create(
        environment=env,
        triggered_by='System Bulk',
        trigger_type='BULK',
        status='RUNNING'
    )
    
    active_games = Game.objects.filter(is_active=True)
    for game in active_games:
        run_game_test.delay(test_run.id, game.id)
