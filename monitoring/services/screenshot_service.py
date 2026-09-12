import os
import uuid
from datetime import datetime
from django.conf import settings

class ScreenshotService:
    def __init__(self):
        # We will use the screenshots folder in the project root
        self.screenshot_dir = os.path.join(settings.BASE_DIR, 'screenshots')
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def generate_filename(self, provider_code: str, game_slug: str, test_id: int) -> str:
        """Generates a filename like kagaming_20000-leagues_10452_20260912_121530.png"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{provider_code}_{game_slug}_{test_id}_{timestamp}_{uuid.uuid4().hex[:6]}.png"

    def get_absolute_path(self, filename: str) -> str:
        """Returns the absolute file system path for the screenshot."""
        return os.path.join(self.screenshot_dir, filename)

    def get_url(self, filename: str) -> str:
        """Returns the URL path to serve the screenshot."""
        return f"/media/screenshots/{filename}"
