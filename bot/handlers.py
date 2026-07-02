import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, filters, MessageHandler

QUESTION, ANSWER = range(2)

logging.basicConfig(
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING) # avoids all GET and POST requests being logged
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    buttons = [
        [KeyboardButton('Add'), KeyboardButton('List')],
        [KeyboardButton('Review'), KeyboardButton('Delete')],
    ]
    reply_markup = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="select an option....."
    )
    help_Text = (
        "- use <b>add</b> to create flashcards\n"
        "- use <b>list</b> to list your flashcards \n"
        "- use <b>review</b> to test yourself with a random card\n"
        "- use <b>delete</b> to remove cards\n"
    )
     
    await update.message.reply_text(text=f"Hi {user.first_name} Welcome \n\n{help_Text}", reply_markup=reply_markup, parse_mode="HTML")

async def add(update: Update, context: ContextTypes):
    await update.message.reply_text("add the front of the flashcard(question or term)", reply_markup=ReplyKeyboardRemove())

    return QUESTION
async def get_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['question'] = update.message.text
    await update.message.reply_text("Great!, now add the back of the flashcard(answer, definition or explanation)")
    return ANSWER
async def get_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text
    await update.message.reply_text("card saved! add another flashcard or type /cancel to return to the main menu") 
    return QUESTION


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = context.user_data.get('question')
    answer = context.user_data.get('answer')

    await update.message.reply_text(f"question: {question} answer: {answer}")

#fallback function
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # re-displays the main menu
    buttons = [
        [KeyboardButton('Add'), KeyboardButton('List')],
        [KeyboardButton('Review'), KeyboardButton('Delete')]
    ]
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, input_field_placeholder="select an option.....")
    await update.message.reply_text('canceled! ', reply_markup=keyboard)
    return ConversationHandler.END


TEXT_ONLY = filters.TEXT & ~filters.COMMAND
conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex('^Add$'), add)],
    states= {
        QUESTION: [MessageHandler(TEXT_ONLY, get_question)],  
        ANSWER: [MessageHandler(TEXT_ONLY, get_answer)]
    },
    fallbacks=[
        CommandHandler('cancel', cancel)
    ]
)


