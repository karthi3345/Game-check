import os
import json
import urllib.request
from typing import Dict, Any

class AlertService:
    def __init__(self):
        self.slack_webhook = os.environ.get('SLACK_WEBHOOK_URL')

    def send_alert(self, game_name: str, status: str, result_data: Dict[str, Any]):
        """Sends an alert for failed or warning test results."""
        if not self.slack_webhook:
            print("AlertService: No SLACK_WEBHOOK_URL configured, skipping alert.")
            return

        color = "#ff0000" if status == "FAIL" else "#ffcc00"
        
        payload = {
            "attachments": [
                {
                    "fallback": f"Test {status}: {game_name}",
                    "color": color,
                    "title": f"Game Monitor Alert: {game_name} ({status})",
                    "text": f"The health check for *{game_name}* resulted in status: *{status}*.",
                    "fields": [
                        {
                            "title": "URL Status",
                            "value": result_data.get('url_check_status', 'N/A'),
                            "short": True
                        },
                        {
                            "title": "Load Time (ms)",
                            "value": str(result_data.get('page_load_time_ms', 'N/A')),
                            "short": True
                        },
                        {
                            "title": "Failure Reason",
                            "value": result_data.get('failure_reason', 'None specified'),
                            "short": False
                        }
                    ],
                    "footer": "Game Health Monitor System"
                }
            ]
        }

        try:
            req = urllib.request.Request(
                self.slack_webhook,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                print(f"Alert sent successfully, response: {response.getcode()}")
        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
