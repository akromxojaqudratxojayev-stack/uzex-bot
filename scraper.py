import asyncio
import json
import os
import re
from playwright.async_api import async_playwright

DATA_FILE = "seen_tenders.json"

def load_seen_tenders():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_seen_tenders(tenders):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tenders, f, indent=4)

def format_beautiful_text(text, category):
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return "", ""
    
    # Lot ID odatda birinchi yoki ikkinchi qatorda bo'ladi
    lot_id = lines[0]
    
    formatted = f"✅ <b>Yangi tender (E-Shop) qo'shildi!</b>\n\n"
    formatted += f"📌 <b>Lot nomi/ID:</b> {lot_id}\n"
    formatted += f"📁 <b>Kategoriya:</b> {category}\n"
    
    # Qolgan ma'lumotlarga mos emojilar qidiramiz
    for line in lines[1:8]: # Asosiy qatorlarni olamiz
        lower_line = line.lower()
        if "summa" in lower_line or "narx" in lower_line or "uzs" in lower_line:
            formatted += f"💰 {line}\n"
        elif "tashkilot" in lower_line or "buyurtmachi" in lower_line:
            formatted += f"🏢 {line}\n"
        elif "muddat" in lower_line or "kun" in lower_line:
            formatted += f"🚚 {line}\n"
        elif "hudud" in lower_line or "manzil" in lower_line:
            formatted += f"📍 {line}\n"
        else:
            formatted += f"🔹 {line}\n"
            
    return lot_id, formatted

async def check_new_tenders(categories):
    new_tenders = []
    seen_ids = load_seen_tenders()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        for item in categories:
            cat = item['category']
            subcat = item['subcategory']
            
            try:
                await page.goto("https://xarid.uzex.uz/shop/products-list/eshop", wait_until="networkidle")
                await page.wait_for_timeout(3000)
                
                category_dropdowns = await page.locator("ng-select").all()
                if len(category_dropdowns) >= 2:
                    await category_dropdowns[0].click()
                    await page.keyboard.type(cat)
                    await page.wait_for_timeout(1000)
                    await page.keyboard.press("Enter")
                    
                    await page.wait_for_timeout(1000)
                    
                    await category_dropdowns[1].click()
                    await page.keyboard.type(subcat)
                    await page.wait_for_timeout(1000)
                    await page.keyboard.press("Enter")

                search_btn = page.locator("button:has-text('Qidirish')")
                if await search_btn.count() > 0:
                    await search_btn.click()
                else:
                    search_btn = page.locator("button:has-text('Поиск')")
                    if await search_btn.count() > 0:
                        await search_btn.click()

                await page.wait_for_timeout(3000)
                
                cards = await page.locator(".card, app-product-card, .product-card, .list-item, .box").all()
                
                for card in cards:
                    try:
                        text_content = await card.inner_text()
                        if not text_content.strip():
                            continue
                            
                        lot_id, pretty_text = format_beautiful_text(text_content, cat)
                        
                        if lot_id and lot_id not in seen_ids:
                            new_tenders.append({
                                "id": lot_id,
                                "text": pretty_text,
                                "link": "https://xarid.uzex.uz/shop/products-list/eshop"
                            })
                            seen_ids.append(lot_id)
                    except Exception as e:
                        pass
            
            except Exception as e:
                pass
                
        await browser.close()
        
    save_seen_tenders(seen_ids)
    return new_tenders
