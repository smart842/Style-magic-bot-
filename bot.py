
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

BOT_TOKEN = os.getenv("7710874384:AAFiFftrfwRIsvGL43TnVmMHWuEwfQa259s")
REPLICATE_API_TOKEN = os.getenv("r8_XeyHtMBI5A8kFhqM2kYhfgcAFJL5ERT2H6pwS")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to StyleMagicBot! Send me a photo to try on clothes.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_file = await update.message.photo[-1].get_file()
    photo_path = "input.jpg"
    await photo_file.download_to_drive(photo_path)

    # Replace with your own Replicate model
    output_url = replicate_tryon(photo_path)
    if output_url:
        await update.message.reply_photo(photo=output_url)
    else:
        await update.message.reply_text("Try-on failed. Please try again later.")

def replicate_tryon(image_path):
    with open(image_path, "rb") as img_file:
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {REPLICATE_API_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "version": "your-model-version-id",
                "input": {"image": image_path}
            }
        )
    if response.ok:
        return response.json().get("output", [None])[0]
    return None

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
