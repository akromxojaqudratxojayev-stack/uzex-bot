import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        print("Navigating to uzex...")
        await page.goto("https://xarid.uzex.uz")
        print("Evaluating API call in page context...")
        result = await page.evaluate("""
            async () => {
                const response = await fetch('https://xarid-api-trade.uzex.uz/api/v2/eshop/product', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({PageSize:10, PageNumber:1})
                });
                return await response.text();
            }
        """)
        print("Result:", result[:500])
        await browser.close()

asyncio.run(run())
