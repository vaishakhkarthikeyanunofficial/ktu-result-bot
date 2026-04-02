import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Check Result"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome! 👋\nClick below to check your result\n\nType /cancel anytime to stop.",
        reply_markup=reply_markup
    )

# HANDLE MESSAGES
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    # CANCEL OPTION
    if text.lower() == "/cancel":
        if user_id in user_data:
            del user_data[user_id]
        await update.message.reply_text("❌ Process cancelled.")
        return

    # START PROCESS
    if text == "Check Result":
        user_data[user_id] = {"step": "username"}
        await update.message.reply_text("Enter your Username:")
        return

    # IF USER NOT STARTED
    if user_id not in user_data:
        await update.message.reply_text("Please click 'Check Result' to start.")
        return

    step = user_data[user_id]["step"]

    # USERNAME STEP
    if step == "username":
        if not text:
            await update.message.reply_text("⚠️ Username cannot be empty.")
            return

        user_data[user_id]["username"] = text
        user_data[user_id]["step"] = "password"
        await update.message.reply_text("Enter your Password:")

    # PASSWORD STEP
    elif step == "password":
        if not text:
            await update.message.reply_text("⚠️ Password cannot be empty.")
            return

        user_data[user_id]["password"] = text
        user_data[user_id]["step"] = "semester"

        keyboard = [["S1", "S2", "S3"], ["S4", "S5", "S6"], ["S7", "S8"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Select Semester:", reply_markup=reply_markup)

    # SEMESTER STEP
    elif step == "semester":
        valid_semesters = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]

        if text not in valid_semesters:
            await update.message.reply_text("⚠️ Please select a valid semester.")
            return

        user_data[user_id]["semester"] = text

        await update.message.reply_text("⏳ Fetching your result...")

        # DUMMY RESULT (will replace with Selenium later)
        await update.message.reply_text(
            f"📊 RESULT:\n\nUsername: {user_data[user_id]['username']}\nSemester: {text}\n\nSGPA: 8.5 (Dummy)"
        )

        # CLEAR DATA AFTER USE
        del user_data[user_id]


# MAIN FUNCTION
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
