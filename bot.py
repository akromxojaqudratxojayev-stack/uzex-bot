import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

import config
from scraper import check_new_tenders

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 <b>Assalomu alaykum!</b>\n\n"
        "🟢 <b>O'zEX E-Shop Avto-Qidiruv Boti ishga tushdi.</b>\n\n"
        "Men endi siz kiritgan toifalarni 24/7 kuzatib boraman va yangi lotlar chiqqanda darhol xabar beraman!",
        parse_mode=ParseMode.HTML
    )

async def background_task():
    while True:
        try:
            logging.info("Tenderlarni tekshirish boshlandi...")
            new_items = await check_new_tenders(config.CATEGORIES)
            
            for item in new_items:
                text = item.get('text')
                text += f"\n\n🔗 <a href='{item.get('link')}'><b>Saytda ko'rish</b></a>"
                try:
                    await bot.send_message(
                        chat_id=config.CHAT_ID,
                        text=text,
                        parse_mode=ParseMode.HTML
                    )
                except Exception as e:
                    logging.error(f"Xabar yuborishda xatolik: {e}")
                    
        except Exception as e:
            logging.error(f"Tekshirish jarayonida xatolik: {e}")
            
        logging.info(f"{config.CHECK_INTERVAL} soniya kutilmoqda...")
        await asyncio.sleep(config.CHECK_INTERVAL)

async def main():
    asyncio.create_task(background_task())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
