"""
Telegram Batch Welcome Bot
==========================
Jaise hi koi naya member group join kare, ye bot:
1. Unhe personally greet karta hai
2. Uday Setty se contact karne ka message deta hai

Setup ke liye niche README padhen.
"""

import logging
from telegram import Update, ChatMember
from telegram.ext import (
    Application,
    ChatMemberHandler,
    ContextTypes,
)

# ─────────────────────────────────────────────
#  YAHAN APNA BOT TOKEN DAALEN
# ─────────────────────────────────────────────
BOT_TOKEN = "APNA_BOT_TOKEN_YAHAN_DAALEN"

# Uday Setty ka Telegram username (@ ke saath)
UDAY_SETTY_USERNAME = "@UdaySetty"  # ← apna real username daalen

# ─────────────────────────────────────────────
#  WELCOME MESSAGE (edit kar sakte hain)
# ─────────────────────────────────────────────
def get_welcome_message(member_name: str) -> str:
    return f"""
🎉 *Swagat hai, {member_name} ji!*

Hamare Batch Group mein aapka dil se swagat hai! 🙏

📚 *Batch ke baare mein jaankari lene ke liye:*
Kripya hamare coordinator *Uday Setty* se directly baat karein:
👉 {UDAY_SETTY_USERNAME}

Unse ye cheezein pooch sakte hain:
• 📅 Batch schedule & timing
• 💰 Fees & payment details  
• 📖 Course syllabus
• ❓ Koi bhi sawaal

Hum chahte hain ki aapki padhai bahut acchi ho! 💪✨
"""

# ─────────────────────────────────────────────
#  BOT LOGIC — kuch badlav ki zaroorat nahi
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Naye member ko greet karta hai."""
    result = update.chat_member

    # Sirf tab chalega jab koi JOIN kare (leave pe nahi)
    if result.new_chat_member.status in [
        ChatMember.MEMBER,
        ChatMember.ADMINISTRATOR,
    ] and result.old_chat_member.status in [
        ChatMember.LEFT,
        ChatMember.BANNED,
        ChatMember.RESTRICTED,
    ]:
        new_user = result.new_chat_member.user
        member_name = new_user.first_name or "Dost"

        welcome_text = get_welcome_message(member_name)

        await context.bot.send_message(
            chat_id=result.chat.id,
            text=welcome_text,
            parse_mode="Markdown",
        )
        logger.info(f"✅ Welcome message bheja: {member_name} ({new_user.id})")


def main():
    """Bot start karta hai."""
    print("🤖 Batch Welcome Bot shuru ho raha hai...")

    app = Application.builder().token(BOT_TOKEN).build()

    # New member join hone par handler
    app.add_handler(ChatMemberHandler(greet_new_member, ChatMemberHandler.CHAT_MEMBER))

    print("✅ Bot chal raha hai! Group mein kisi ko join karo aur dekho...")
    app.run_polling(allowed_updates=["chat_member"])


if __name__ == "__main__":
    main()
