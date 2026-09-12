import asyncio
from playwright.async_api import async_playwright

async def fetch_website():
    print("Starting Playwright to fetch https://myvepower.com/ ...")
    async with async_playwright() as p:
        # Launch Chromium headless
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("Navigating to https://myvepower.com/ ...")
            response = await page.goto("https://myvepower.com/", timeout=30000)
            
            print(f"Status Code: {response.status}")
            print(f"Page Title: {await page.title()}")
            
            # Take a screenshot
            screenshot_path = "screenshots/myvepower_test.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot successfully saved to: {screenshot_path}")
            
        except Exception as e:
            print(f"Error fetching website: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(fetch_website())
