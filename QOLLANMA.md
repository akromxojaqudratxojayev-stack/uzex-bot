# Uzex E-Shop Telegram Bot

Bu bot O'zbekiston Respublikasi tovar-xomashyo birjasining elektron do'koni (xarid.uzex.uz/shop/products-list/eshop) dagi belgilangan toifalarni avtomatik tarzda kuzatib boradi. Yangi tenderlar/lotlar paydo bo'lsa, sizning Telegramingizga xabar yuboradi.

## O'rnatish tartibi

1. **Telegram bot ochish:**
   - Telegramga kiring va qidiruvga `@BotFather` deb yozing.
   - `/newbot` buyrug'ini bering.
   - Botga ism va username (masalan, `uzex_mening_bot`) bering.
   - BotFather sizga **TOKEN** (masalan, `123456789:ABCDefgh...`) beradi. Buni saqlab qo'ying.

2. **Sozlamalarni kiritish:**
   - `config.py` faylini oching.
   - `BOT_TOKEN = "..."` qismiga BotFather bergan tokenni yozing.
   - `CHAT_ID = "..."` qismiga o'zingizning Telegram ID raqamingizni yozing (Buni `@userinfobot` kabi botlar orqali bilib olishingiz mumkin).

3. **Kerakli kutubxonalarni o'rnatish:**
   - Terminal (CMD yoki PowerShell) da ushbu papkaga kiring:
     ```bash
     cd C:\Users\UNICON-SOFT\Desktop\programma\uzex_bot
     ```
   - Quyidagi buyruqlarni yozib, kerakli dasturlarni o'rnating:
     ```bash
     pip install -r requirements.txt
     playwright install chromium
     ```

4. **Botni ishga tushirish:**
   - Terminalda quyidagi buyruqni bering:
     ```bash
     python bot.py
     ```
   - Telegramda botingizga kirib `/start` tugmasini bosing.

Diqqat: Saytning strukturasi vaqt o'tishi bilan o'zgarishi mumkin. Bunday holatda `scraper.py` ichidagi HTML-klasslar ("ng-select", ".card") nomini moslashtirish kerak bo'ladi.
