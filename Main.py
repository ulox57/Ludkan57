import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "9285396228:AAHZWPJe8t85oqNUCTiYKz2aDWxQax5B65I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

TEXTS = {
    "ua": {
        "welcome": "Привіт! Оберіть мову / Choose your language:",
        "main_menu": "🎰 Ласкаво просимо до Лудки!\n\nОберіть гру нижче:",
        "spin_slots": "🎰 Крутити Слоти",
        "throw_darts": "🎯 Кинути Дартс",
        "change_lang": "🌐 Змінити мову",
        "slots_win": "🎉 JACKPOT! 777 WINNER!\n\n👑 Гравець: {name}\n🎁 Приз: 25 Telegram Stars\n\n👤 Адмін @M7aq10, перевірте виграш вручну.",
        "slots_lose": "😢 Спробуй ще раз! Тобі випало не 777.",
        "darts_center": "🎯 ЧИСТЕ ВЛУЧАННЯ В ЦЕНТР!\n\n👑 Гравець: {name}\n🎁 Приз: 25 Telegram Stars\n\n👤 Адмін @M7aq10, перевірте виграш вручну.",
        "darts_lose": "🔘 Майже! Але не центр. Спробуй ще раз!"
    },
    "en": {
        "welcome": "Hello! Choose your language / Оберіть мову:",
        "main_menu": "🎰 Welcome to the Gambling Bot!\n\nChoose your game below:",
        "spin_slots": "🎰 Spin Slots",
        "throw_darts": "🎯 Throw Darts",
        "change_lang": "🌐 Change Language",
        "slots_win": "🎉 JACKPOT! 777 WINNER!\n\n👑 Player: {name}\n🎁 Prize: 25 Telegram Stars\n\n👤 Admin @M7aq10, check the win manually.",
        "slots_lose": "😢 Try again! You didn't get 777.",
        "darts_center": "🎯 DIRECT HIT TO THE CENTER!\n\n👑 Player: {name}\n🎁 Prize: 25 Telegram Stars\n\n👤 Admin @M7aq10, check the win manually.",
        "darts_lose": "🔘 Close! But not the center. Try again!"
    }
}

user_lang = {}

def get_menu_kb(lang):
    kb = InlineKeyboardBuilder()
    kb.button(text=TEXTS[lang]["spin_slots"], callback_data="play_slots")
    kb.button(text=TEXTS[lang]["throw_darts"], callback_data="play_darts")
    kb.button(text=TEXTS[lang]["change_lang"], callback_data="choose_lang")
    kb.adjust(1)
    return kb.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇦 Українська", callback_data="set_lang_ua")
    kb.button(text="🇬🇧 English", callback_data="set_lang_en")
    await message.answer(TEXTS["ua"]["welcome"], reply_markup=kb.as_markup())

@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[-1]
    user_lang[callback.from_user.id] = lang
    await callback.message.edit_text(TEXTS[lang]["main_menu"], reply_markup=get_menu_kb(lang))
    await callback.answer()

@dp.callback_query(F.data == "choose_lang")
async def change_language(callback: types.CallbackQuery):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇺🇦 Українська", callback_data="set_lang_ua")
    kb.button(text="🇬🇧 English", callback_data="set_lang_en")
    await callback.message.edit_text(TEXTS["ua"]["welcome"], reply_markup=kb.as_markup())
    await callback.answer()

@dp.callback_query(F.data == "play_slots")
async def play_slots(callback: types.CallbackQuery):
    lang = user_lang.get(callback.from_user.id, "ua")
    msg = await callback.message.answer_dice(emoji="🎰")
    await asyncio.sleep(4)
    if msg.dice.value == 64:
        await msg.reply(TEXTS[lang]["slots_win"].format(name=callback.from_user.full_name))
    else:
        await msg.reply(TEXTS[lang]["slots_lose"])
    await callback.answer()

@dp.callback_query(F.data == "play_darts")
async def play_darts(callback: types.CallbackQuery):
    lang = user_lang.get(callback.from_user.id, "ua")
    msg = await callback.message.answer_dice(emoji="🎯")
    await asyncio.sleep(4)
    if msg.dice.value == 6:
        await msg.reply(TEXTS[lang]["darts_center"].format(name=callback.from_user.full_name))
    else:
        await msg.reply(TEXTS[lang]["darts_lose"])
    await callback.answer()

async def handle(request):
    return web.Response(text="Бот працює!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 10000)
    asyncio.create_task(site.start())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
