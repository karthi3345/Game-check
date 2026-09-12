import asyncio
from playwright.async_api import async_playwright

async def check_myvepower_games():
    print("Starting Game Checker for https://myvepower.com/ ...")
    async with async_playwright() as p:
        # Launch Chromium headless
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("1. Opening MyVepower website...")
            await page.goto("https://myvepower.com/", timeout=30000)
            
            # Wait for the page to load
            await page.wait_for_timeout(3000)
            
            print("2. Scanning for Game Links...")
            # This attempts to find elements that look like game links
            game_links = await page.locator("a[href*='/game'], a[href*='/play']").all()
            
            if len(game_links) == 0:
                print("   -> No direct game links found on the homepage. They might be behind a login screen.")
            else:
                print(f"   -> Found {len(game_links)} potential games!")
                for link in game_links[:3]: # check first 3
                    url = await link.get_attribute("href")
                    print(f"   -> Found game link: {url}")
            
            print("3. Taking a screenshot of the main lobby...")
            await page.screenshot(path="screenshots/lobby_status.png", full_page=True)
            print("   -> Screenshot saved! (Check 'screenshots/lobby_status.png')")
            
        except Exception as e:
            print(f"Error checking games: {e}")
        finally:
            await browser.close()
            print("Finished checking.")

if __name__ == "__main__":
    asyncio.run(check_myvepower_games())
