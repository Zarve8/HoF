import telebot
from img import load_user_preview
from processor import process_image
from instagram import start as start_insta, publish_image
import os


bot = telebot.TeleBot('6112948555:AAE7dI3CTPn_gHPu6YWzX8gA8yAoWRIC7dw')
start_insta()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi, I am HoF bot")
    bot.send_message(message.chat.id, "commands")
    bot.send_message(message.chat.id, "/paint Paint your sketch to the virtual wall")
    bot.send_message(message.chat.id, "/publish Publish your work to instagram")
    bot.send_message(message.chat.id, "/preview Show last processed image to be published")


@bot.message_handler(commands=['paint'])
def paint(message):
    bot.send_message(message.chat.id, "Send me a photo of your sketch, it must have clear bounds. "
                                      "Do not use hollow sketches of the same color as background. "
                                      "Send ony compressed photos.")
    bot.send_message(message.chat.id, "You would be able to preview your work before publishing")


@bot.message_handler(content_types=['photo'])
def paint_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filepath = "files/work_raw_"+message.chat.id.__str__()+".png"
    with open(filepath, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, "Processing")
    filepath = process_image(filepath, message.chat.id)
    bot.send_chat_action(message.chat.id, 'upload_photo')
    img = open(filepath, 'rb')
    bot.send_message(message.chat.id, "Preview of your work")
    bot.send_photo(message.chat.id, img)
    img.close()


@bot.message_handler(commands=['preview'])
def preview(message):
    img = load_user_preview(message.chat.id)
    if img is None:
        bot.send_message(message.chat.id, "You have no sketches to publish")
        return
    else:
        bot.send_message(message.chat.id, "Preview of your work")
        bot.send_photo(message.chat.id, img)
        img.close()


@bot.message_handler(commands=['publish'])
def publish(message):
    filepath = "files/work_on_wall_" + message.chat.id.__str__() + ".jpg"
    if os.path.exists(filepath):
        bot.send_message(message.chat.id, "Start publishing")
        publish_image(filepath)
        bot.send_message(message.chat.id, "Your sketch was published to virtual wall")
    else:
        bot.send_message(message.chat.id, "You have no sketches to publish")


bot.infinity_polling()
