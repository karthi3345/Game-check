import os
import time
from typing import Dict, Any
from playwright.sync_api import sync_playwright
from django.conf import settings

class BrowserService:
    def __init__(self, environment_config):
        self.config = environment_config
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def start(self):
        """Initializes Playwright and the browser."""
        self.playwright = sync_playwright().start()
        
        launch_options = {
            'headless': self.config.headless,
            'args': ['--no-sandbox', '--disable-setuid-sandbox']
        }
        
        if self.config.browser.lower() == 'firefox':
            self.browser = self.playwright.firefox.launch(**launch_options)
        elif self.config.browser.lower() == 'webkit':
            self.browser = self.playwright.webkit.launch(**launch_options)
        else:
            self.browser = self.playwright.chromium.launch(**launch_options)
            
        self.context = self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            record_video_dir=None
        )
        self.page = self.context.new_page()

    def login(self) -> bool:
        """Logs into the target platform using credentials from the environment."""
        if not self.config.login_credentials_env_key:
            return True # No login required
            
        creds = os.environ.get(self.config.login_credentials_env_key)
        if not creds:
            print(f"Warning: Login credentials key '{self.config.login_credentials_env_key}' not found in environment.")
            return False
            
        try:
            username, password = creds.split(':', 1)
        except ValueError:
            print("Error: Credentials must be in format 'username:password'")
            return False

        try:
            self.page.goto(self.config.base_url, wait_until='networkidle')
            
            # NOTE: These are generic fallback selectors. 
            # They should be updated based on the actual myvepower.com login UI.
            
            # Try to click a login button if we are not already on the login form
            try:
                self.page.locator('text="Log In", text="Login", .dash-btn-login').first.click(timeout=3000)
                self.page.wait_for_timeout(1000)
            except:
                pass
                
            self.page.fill('input[type="text"], input[name="username"], input[name="email"]', username)
            self.page.fill('input[type="password"]', password)
            self.page.click('button[type="submit"], input[type="submit"], button:has-text("Login")')
            
            # Wait for navigation / state change after login
            self.page.wait_for_load_state('networkidle', timeout=15000)
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False

    def navigate_to_game(self, game_url: str) -> Dict[str, Any]:
        """Navigates to the specific game and returns loading metrics."""
        result = {
            'url_check_status': 'FAIL',
            'http_status_code': None,
            'page_load_status': 'FAIL',
            'page_load_time_ms': None
        }
        
        try:
            start_time = time.time()
            response = self.page.goto(game_url, wait_until='domcontentloaded', timeout=self.config.launch_timeout_seconds * 1000)
            
            if response:
                result['http_status_code'] = response.status
                result['url_check_status'] = 'PASS' if response.ok else 'FAIL'
                
            self.page.wait_for_load_state('networkidle', timeout=10000)
            
            load_time = int((time.time() - start_time) * 1000)
            result['page_load_time_ms'] = load_time
            result['page_load_status'] = 'PASS'
            
        except Exception as e:
            print(f"Navigation failed: {e}")
            
        return result

    def close(self):
        """Cleans up browser resources."""
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
