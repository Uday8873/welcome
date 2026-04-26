"""
Telegram Batch Welcome Bot
"""

import os
import sys
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, ChatMember
from telegram.ext import (
    Application,
    ChatMemberHandler,
    ContextTypes,
)

# ─────────────────────────────────────────────
#  BOT TOKEN CHECK
# ─────────────────────────────────────────────
BOT_TOKEN = os.environ.get("8772470673:AAFn2Wu-IkN4RjXWVYwqlQJfHIX-qHfUD8A")

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable set nahi hai!")
    print("Render Dashboard → Environment → BOT_TOKEN add karein")
    sys.exit(1)

print(f"✅ BOT_TOKEN mila: {BOT_TOKEN[:10]}...")

# Uday Setty ka Telegram username
UDAY_SETTY_USERNAME = "@UdaySetty"

# ─────────────────────────────────────────────
#  WELCOME MESSAGE
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
#  RENDER KE LIYE DUMMY WEB SERVER
# ─────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

    def log_message(self, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 Web server port {port} par chal raha hai...")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

# ─────────────────────────────────────────────
#  BOT LOGIC
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member

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
    print("🤖 Batch Welcome Bot shuru ho raha hai...")

    # Web server pehle start karo
    threading.Thread(target=run_server, daemon=True).start()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(ChatMemberHandler(greet_new_member, ChatMemberHandler.CHAT_MEMBER))

    print("✅ Bot polling shuru...")
    app.run_polling(allowed_updates=["chat_member"])


if __name__ == "__main__":
    main()
