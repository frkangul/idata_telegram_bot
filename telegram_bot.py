import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from find_idata_randevu import find_randevu

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="iData dan randevu bulacak botum. /randevu_ara komutu ile istanbul içinde standart hizmet için 2 kişilik radevu arar. Uygun randevu bulunca mesaj atar. İstanbul içinde prime hizmet için randevu almak istiyorsanız /prime_radevu_ara kullan.")

async def randevu_ara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Randevu aranmaya baslandi!")
    while True:
        location, code = find_randevu()
        if code == 1:
            logging.info(f"{location} da randevu bulundu! Bot aramayi durdurdu.")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{location} da randevu bulundu! Bot aramayi durdurdu.")
            break  # Exit the loop if a valid randevu is found
        elif code == -1:
            logging.info(f"{location} da randevu bulunmuş olabilir! Bot aramaya devam ediyor.")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{location} da randevu bulunmuş olabilir! Bot aramaya devam ediyor.")
            await asyncio.sleep(60)  # Wait for 60 seconds before retrying

async def prime_radevu_ara(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # to be imlemented
    location = find_randevu(hizmet = "prime")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{location} da randevu bulundu!")


if __name__ == '__main__':
    application = ApplicationBuilder().token('7193540098:AAH29AUB0eXpwUi2FVGSDHZ2enyrWff4mFM').build()
    
    start_handler = CommandHandler('start', start)
    randevu_ara_handler = CommandHandler('randevu_ara', randevu_ara)
    # prime_radevu_arahandler = CommandHandler('prime_radevu_ara', prime_radevu_ara)
    application.add_handler(start_handler)
    application.add_handler(randevu_ara_handler)
    
    application.run_polling()