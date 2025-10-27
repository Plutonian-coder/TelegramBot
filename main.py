import os
import logging
import google.generativeai as genai
# Note: The package is installed as 'python-dotenv', but imported as 'dotenv' 
# or 'python_dotenv'. Using 'dotenv' is usually fine, but 'python_dotenv' is safer if you had issues.
from dotenv import load_dotenv 

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Set up logging to print to console (which you are already doing correctly)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Configure Gemini API
load_dotenv() # Loads GOOGLE_API_KEY from .env file
try:
    # 1. Retrieve the value from the environment
    api_key = os.getenv('GOOGLE_API_KEY') 
    
    # 2. Check if the key was found
    if not api_key:
        # This will trigger the exception if the .env file or key is missing
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")

    # 3. Pass the *value* to genai.configure()
    genai.configure(api_key=api_key)
    
    # Configure and load the model
    gemini_model = genai.GenerativeModel(
        'gemini-2.5-flash',
        system_instruction="You are GEEKGURU, a badass tech expert chatbot created by Khalid Yekini. You're a master in problem solving, computing, coding, and all things tech. Provide detailed, accurate, and formatted responses using Markdown. Be confident, helpful, and focus only on technology topics. If asked about non-tech, redirect to tech with style."
    )
    logging.info("Gemini API configured successfully.")
except Exception as e:
    # This will log if the API key is missing or invalid
    logging.error(f"Failed to configure Gemini API: {e}")
    gemini_model = None

# Define a few command handlers. 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # Using MarkdownV2 requires escaping specific characters
    await update.message.reply_markdown_v2(
        f"🚀 **Greetings, {user.mention_markdown_v2()}!**\n\n"
        "I'm *GEEKGURU*, your badass tech expert! 💻\n"
        "Ready to crush coding problems, solve computing mysteries, and dive deep into tech? Let's geek out! 🤓"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_markdown_v2(
        "🤖 **GEEKGURU** \\- The Ultimate Tech Bot\n\n"
        "Created by *Khalid Yekini* 🧑‍💻\n\n"
        "**What I do:**\n"
        "• Problem\\-solving wizard 🧙‍♂️\n"
        "• Computing expert 💾\n"
        "• Coding master 🐍\n"
        "• Tech discussion dominator 💬\n\n"
        "**Commands:**\n"
        "/start \\- Get started\n"
        "/help \\- This help message\n\n"
        "Ask me anything tech\\-related! 🔥"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message or get response from Gemini."""
    user_text = update.message.text.lower()
    if "who created" in user_text or "creator" in user_text:
        await update.message.reply_markdown_v2("I am *GEEKGURU*, created by **Khalid Yekini**! 🧑‍💻")
        return

    if gemini_model:
        try:
            response = gemini_model.generate_content(update.message.text)
            # Ensure the response text is properly escaped for MarkdownV2, as it comes from the LLM
            # (Note: This is a complex step, often requiring a utility function, but we use the basic reply_text for safety)
            await update.message.reply_text(response.text) 
        except Exception as e:
            logging.error(f"Error generating content from Gemini: {e}")
            await update.message.reply_text("Sorry, I couldn't generate a response at this time.")
    else:
        await update.message.reply_text("Gemini API is not configured. I can only echo messages.")


# Directly assign the provided token.
TOKEN = "7351415792:AAF3QEvGPDeoqfdwoY_poHR4vo2KRsuEL8Y"

if not TOKEN or TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
    logging.error("TELEGRAM_BOT_TOKEN not found or is the placeholder string. Please replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual token.")
else:
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # --- DEBUGGING STEP: Print before polling starts ---
    print("Bot initialized! Starting network polling...")
    
    # This call runs forever (or until an unrecoverable network/token error)
    application.run_polling(poll_interval=3.0)

# The script should not reach this point unless the polling loop is interrupted or fails.
print("Bot process stopped.")
