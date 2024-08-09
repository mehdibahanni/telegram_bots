import os
from rembg import remove
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = '7472471896:AAEqC-7kahxwz1MjwOP_o_-5XIwi-8uRV8M'

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Hi, I am remove background bot. To start, click /start')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Send the image to remove background')

async def process_image(photo_name: str):
    name, _ = os.path.splitext(photo_name)
    output_photo_path = f'./processed/{name}.png'
    input_image = Image.open(f'./temp/{photo_name}')
    output = remove(input_image)
    output.save(output_photo_path)
    os.remove(f'./temp/{photo_name}')
    return output_photo_path

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if filters.PHOTO.check_update(update):
        file_id = update.message.photo[-1].file_id
        unique_id = update.message.photo[-1].file_unique_id
        photo_name = f'{unique_id}.jpg'
    elif update.message.document and update.message.document.mime_type.startswith('image/'):
        file_id = update.message.document.file_id
        _, f_ext = os.path.splitext(update.message.document.file_name)
        unique_id = update.message.document.file_unique_id
        photo_name = f'{unique_id}{f_ext}'  # Use .{f_ext} without the dot before extension

    photo_file = await context.bot.get_file(file_id)
    await photo_file.download_to_drive(custom_path=f'./temp/{photo_name}')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Image is being processed')
    processed_image = await process_image(photo_name)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(processed_image, 'rb'))
    os.remove(processed_image)

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('./temp', exist_ok=True)
    os.makedirs('./processed', exist_ok=True)

    application = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    help_handler = CommandHandler('help', help)
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_message)

    # Register handlers
    application.add_handler(help_handler)
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    # Run the application
    application.run_polling()





























# from telegram.ext import Updater, CommandHandler
# import requests

# # Replace 'your_bot_token_here' with your actual bot token
# TOKEN = 'your_bot_token_here'

# def start(update, context):
#     update.message.reply_text('Bot started! Listening for new services on Khamsat.')

# def check_new_services():
#     # Implement your logic to check for new services on Khamsat
#     # Example: Fetch new services using requests library
#     response = requests.get('https://khamsat.com/community/requests')
#     # Process the response and check for new services

#     # For demonstration, assume new services are found
#     new_services = ['Service 1', 'Service 2', 'Service 3']
#     return new_services

# def send_new_services(update, context):
#     new_services = check_new_services()
#     if new_services:
#         update.message.reply_text(f'New services added to Khamsat: {", ".join(new_services)}')
#     else:
#         update.message.reply_text('No new services found.')

# def main():
#     updater = Updater(TOKEN, use_context=True)
#     dp = updater.dispatcher

#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("checkservices", send_new_services))

#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()

# import telegram
# import asyncio

# TOKEN = '7472471896:AAEqC-7kahxwz1MjwOP_o_-5XIwi-8uRV8M'

# async def main():
#     bot = telegram.Bot(TOKEN)
#     last_update_id = None
    
#     async with bot:
#         while True:
#             updates = await bot.get_updates(offset=last_update_id)
            
#             if updates:
#                 for update in updates:
#                     last_update_id = update.update_id + 1
#                     if update.message:
#                         chat_id = update.message.chat.id
#                         user_name = update.message.from_user.first_name
#                         await bot.send_message(text=f'Hi {user_name}!', chat_id=chat_id)
            
#             await asyncio.sleep(5)  # Check for updates every 5 seconds

# if __name__ == '__main__':
#     asyncio.run(main())
