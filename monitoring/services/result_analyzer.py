from typing import Dict, Any

class ResultAnalyzer:
    def calculate_final_status(self, result: Dict[str, Any]) -> str:
        """
        Calculates the final PASS/WARNING/FAIL status based on the individual checks.
        
        PASS if:
        - URL reachable
        - game launch successful
        - game screen detected
        - no critical loading failure
        - screenshot captured
        - OCR completed
        - expected text found when configured
        - no critical API/network failure
        
        WARNING if:
        - game launches and screen appears, but non-critical console/network warnings exist
        - OR loading time exceeds warning threshold
        
        FAIL if:
        - URL cannot be reached
        - launch fails
        - timeout
        - game screen not detected
        - critical error text detected
        - critical API request failed
        - expected text is missing when required
        - browser/page crashes
        """
        
        # Determine failure conditions
        if result.get('url_check_status') == 'FAIL':
            return 'FAIL'
            
        if result.get('page_load_status') == 'FAIL':
            return 'FAIL'
            
        if result.get('launch_status') == 'FAIL':
            return 'FAIL'
            
        if result.get('game_screen_status') == 'FAIL':
            return 'FAIL'
            
        if result.get('expected_text_status') == 'FAIL':
            return 'FAIL'
            
        # Error messages detected in OCR
        if result.get('ocr_status') == 'FAIL':
            return 'FAIL'

        # Check for critical network errors (e.g. 401, 403, 500)
        network_errors = result.get('network_errors', [])
        for err in network_errors:
            if err.get('status') in [401, 403, 404, 500]:
                return 'FAIL'
                
        # Determine warning conditions
        console_errors = result.get('console_errors', [])
        if len(console_errors) > 0:
            return 'WARNING'
            
        if len(network_errors) > 0:
            return 'WARNING'
            
        load_time = result.get('page_load_time_ms', 0)
        launch_time = result.get('launch_time_ms', 0)
        
        # Arbitrary warning thresholds for load times
        if load_time > 15000 or launch_time > 20000:
            return 'WARNING'
            
        return 'PASS'
