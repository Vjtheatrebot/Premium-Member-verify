from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor
import config

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(msg: types.Message):
    await msg.answer(
        "👋 Welcome! You're interested in joining our *Premium Channel*.\n\n"
        "💰 Subscription: ₹50/month\n"
        "📤 Send UPI payment to `your-upi-id@upi`\n"
        "📸 After payment, send a screenshot here.\n\n"
        "✅ Once verified, you’ll get the invite link.",
        parse_mode="Markdown"
    )

@dp.message_handler(content_types=['photo', 'document'])
async def payment_proof(msg: types.Message):
    await msg.forward(config.ADMIN_USER_ID)
    await msg.reply("✅ Payment screenshot received! Waiting for admin confirmation...")

@dp.message_handler(lambda m: m.text.lower() == "confirm" and str(m.from_user.id) == str(config.ADMIN_USER_ID))
async def admin_confirm(msg: types.Message):
    if msg.reply_to_message:
        user_id = msg.reply_to_message.forward_from.id
        await bot.send_message(user_id, f"✅ Your payment has been verified!\nHere is your invite link:\n{config.CHANNEL_INVITE_LINK}")
        await msg.reply("User confirmed and invited.")
