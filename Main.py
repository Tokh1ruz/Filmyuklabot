import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command

BOT_TOKEN = "BOT_TOKEN_HERE"  # O'zingizning tokeningizni shu yerga joylashtiring
ADMIN_ID = 123456789  # O'z Telegram ID'ingizni bu yerga qo'ying
REQUIRED_CHANNELS = ['@lacoreuzbekistan1']

videos = {}  # { 'kod123': 'video_file_id' }

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def check_subscriptions(user_id):
    for channel in REQUIRED_CHANNELS:
        chat_member = await bot.get_chat_member(channel, user_id)
        if chat_member.status not in ['member', 'creator', 'administrator']:
            return False
    return True

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    if await check_subscriptions(message.from_user.id):
        await message.answer("Xush kelibsiz! Iltimos, videoni olish uchun kod yuboring.")
    else:
        text = "Iltimos, quyidagi kanalga obuna bo'ling:
"
        for ch in REQUIRED_CHANNELS:
            text += f"{ch}\n"
        text += "\nObuna boâlib boâlgach, /start ni qayta yuboring."
        await message.answer(text)

@dp.message(Command("add"))
async def add_video_command(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Foydalanish: /add kod123")
        return
    code = parts[1]
    await message.answer("Endi video faylni yuboring.")

    @dp.message(F.video)
    async def get_video(msg: types.Message):
        if msg.from_user.id == ADMIN_ID:
            file_id = msg.video.file_id
            videos[code] = file_id
            await msg.answer(f"Video '{code}' kodi bilan saqlandi.")
        else:
            await msg.answer("Sizga ruxsat yoâq.")

@dp.message()
async def handle_code(message: types.Message):
    if not await check_subscriptions(message.from_user.id):
        await message.answer("Iltimos, avval kanalga aâzo boâling.")
        return
    
    code = message.text.strip()
    if code in videos:
        await message.answer_video(videos[code])
    else:
        await message.answer("Bunday kod mavjud emas.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
