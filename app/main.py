import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Connect OpenAI client to Groq's free endpoint
openai_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salutations! Welcome to your bilingual Telegram tutor. Send me any text message in English or French!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # 1. Initialize the memory bank on their first message
    if "history" not in context.user_data:
        system_prompt = """You are a strict French DELF B2 examiner and bilingual tutor. 
Evaluate the user's input. If they speak French, reply entirely in French.
Rules:
1. Correct any grammar or spelling mistakes.
2. EXPLICITLY highlight tricky phonetic liaisons, silent letters, or complex vowel morphs (like EU, EAU, OI, or -ER/-É).
3. Format your response exactly like this:
🎯 **Correction:** [Corrected text or "Parfait !"]
💡 **Explanation:** [Grammar AND phonetic/pronunciation breakdown]
💬 **Reply:** [Natural conversational follow-up to keep them talking]"""
        
        context.user_data["history"] = [
            {"role": "system", "content": system_prompt}
        ]

    # 2. Append the new message to history
    context.user_data["history"].append({"role": "user", "content": user_text})

    # 3. Buffer control (Keep system prompt at index 0, limit to last 10 interactions)
    if len(context.user_data["history"]) > 11:
        context.user_data["history"].pop(1)
        context.user_data["history"].pop(1)

    # 4. Call Groq with the full conversational history
    try:
        # I updated the model name to a standard fast Groq model
        response = openai_client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"), 
            messages=context.user_data["history"],
            temperature=0.7
        )
        
        tutor_reply = response.choices[0].message.content
        
        # 5. Save the bot's reply into memory so it remembers context next time
        context.user_data["history"].append({"role": "assistant", "content": tutor_reply})
        
        await update.message.reply_text(tutor_reply, parse_mode="Markdown")
        
    except Exception as e:
        logging.error(f"API Error: {e}")
        await update.message.reply_text("Désolé, mon moteur de réflexion a planté. Peux-tu répéter ?")
if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    app.run_polling()
