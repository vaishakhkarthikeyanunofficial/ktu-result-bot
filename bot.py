import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Check Result"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome! 👋\nClick below to check your result",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "Check Result":
        user_data[user_id] = {"step": "username"}
        await update.message.reply_text("Enter your Username:")

    elif user_id in user_data:
        step = user_data[user_id]["step"]

        if step == "username":
            user_data[user_id]["username"] = text
            user_data[user_id]["step"] = "password"
            await update.message.reply_text("Enter your Password:")

        elif step == "password":
            user_data[user_id]["password"] = text
            user_data[user_id]["step"] = "semester"

            keyboard = [["S1", "S2", "S3"], ["S4", "S5", "S6"], ["S7", "S8"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            await update.message.reply_text(
                "Select Semester:",
                reply_markup=reply_markup
            )

        elif step == "semester":
            user_data[user_id]["semester"] = text

            await update.message.reply_text("⏳ Fetching your result...")

            # Dummy output (replace later with Selenium)
            await update.message.reply_text(
                f"📊 RESULT:\n\nUsername: {user_data[user_id]['username']}\nSemester: {text}\n\nSGPA: 8.5 (Dummy)"
            )

            # Clear user data (important for security)
            del user_data[user_id]


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
