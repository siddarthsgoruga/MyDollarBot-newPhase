#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import telebot
import time
import helper
import edit
import history
import display
import estimate
import delete
import add
import budget
import category
import income
import add_recurring
import summary
from datetime import datetime
from jproperties import Properties

# Load configuration from user.properties
configs = Properties()

with open('user.properties', 'rb') as read_prop:
    configs.load(read_prop)

# Get the API token from the configuration
api_token = str(configs.get('api_token').data)

# Create a Telegram bot using the API token
bot = telebot.TeleBot(api_token)

# Set the log level for the telebot library
telebot.logger.setLevel(logging.INFO)

# Dictionary to store user options
option = {}


# Define listener for requests by user
def listener(user_requests):
    for req in user_requests:
        if(req.content_type == 'text'):
            # Print information about incoming messages
            print("{} name:{} chat_id:{} \nmessage: {}\n".format(str(datetime.now()), str(req.chat.first_name), str(req.chat.id), str(req.text)))


bot.set_update_listener(listener)


# Handle the /start and /menu commands
@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    helper.read_json()
    global user_list
    chat_id = m.chat.id

    text_intro = "Welcome to MyDollarBot - a simple solution to track your expenses and manage them ! \nPlease select the options from below for me to assist you with: \n\n"
    commands = helper.getCommands()
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True


# Handle the /exit command
@bot.message_handler(commands=['exit'])
def exit_command(m):
    helper.read_json()
    global user_list
    chat_id = m.chat.id
    text_intro = "Exited from MyDollarBot ! Thank you for using MyDollarBot to track your expenses!\nIf you ever need to track expenses again, select "
    commands = helper.getExitCommands()
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + " to "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True


# Handle the /add command to add an expense
@bot.message_handler(commands=['add'])
def command_add(message):
    add.run(message, bot)


# Handle the /add_recurring command to add recurring expenses
@bot.message_handler(commands=['add_recurring'])
def command_add_recurring(message):
    add_recurring.run(message, bot)
    
    
# Handle the /history command to fetch expenditure history of the user
@bot.message_handler(commands=['history'])
def command_history(message):
    history.run(message, bot)


# Handle the /edit command to edit date, category, or cost of a transaction
@bot.message_handler(commands=['edit'])
def command_edit(message):
    edit.run(message, bot)


# Handle the /display command to display total expenditure
@bot.message_handler(commands=['display'])
def command_display(message):
    display.run(message, bot)


# Handle the /estimate command to estimate future expenditure
@bot.message_handler(commands=['estimate'])
def command_estimate(message):
    estimate.run(message, bot)


# Handle the /delete command
@bot.message_handler(commands=['delete'])
def command_delete(message):
    delete.run(message, bot)

# Handle the /budget command
@bot.message_handler(commands=['budget'])
def command_budget(message):
    budget.run(message, bot)

# Handle the /category command
@bot.message_handler(commands=['category'])
def command_category(message):
    category.run(message, bot)
    
# Handle the /income command    
@bot.message_handler(commands=['income'])
def command_income(message):
    income.run(message, bot)

# Handle the /summary command
@bot.message_handler(commands=['summary'])
def command_category(message):
    summary.run(message, bot)

# Handle incoming messages that are not commands
@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document','text', 'location', 'contact', 'sticker'])
def default_command(message):
    chat_id = message.chat.id
    text_intro = "Sorry! There is no such option "+message.text+". Choose an option only from given menu.\nSelect "
    commands = helper.getExitCommands()
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + " to "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True
    
# Main function to start the bot
def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")


if __name__ == '__main__':
    main()
