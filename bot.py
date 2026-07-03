import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje_usuario = update.message.text

    respuesta = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": mensaje_usuario}]
        }
    ).json()

    texto = respuesta["choices"][0]["message"]["content"]
    await update.message.reply_text(texto)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
app.run_polling()
