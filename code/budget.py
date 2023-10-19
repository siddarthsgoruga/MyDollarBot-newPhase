import helper # Import the helper module for utility functions
import budget_view # Import the budget_view module for viewing the budget
import budget_update #import the budget_update module for updating the budget
import budget_delete # Import the budget_delete module for deleting budget items
import logging # Import the logging module for error handling
from telebot import types # Import types module from the telebot library for user interface


# Define a function to start the budget management process
def run(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    
    # Get available options from the helper module
    options = helper.getOptions()
    markup.row_width = 2
    
    # Add the available budget management options to the keyboard
    for c in options.values():
        markup.add(c)
    
    # Ask the user to select a budget management operation or cancel the operation
    msg = bot.reply_to(message, 'Select Operation or Select Cancel to cancel the operation', reply_markup=markup)
    
    # Register the next step handler to process the user's choice
    bot.register_next_step_handler(msg, post_operation_selection, bot)

# Define a function to handle the user's selected budget management operation
def post_operation_selection(message, bot):
    try:
        chat_id = message.chat.id
        op = message.text
        
        # Get available options from the helper module
        options = helper.getOptions()
        
        # Check if the selected operation is valid
        if op not in options.values():
            # If the user selected "update," run the budget_update module
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this operation \"{}\"!".format(op))
        if op == options['update']:
            budget_update.run(message, bot)
        elif op == options['view']:
            budget_view.run(message, bot)
        elif op == options['delete']:
            budget_delete.run(message, bot)
        elif op == options['cancel']:
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(chat_id, text_intro)
        else :
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this operation \"{}\"!".format(op))

    except Exception as e:
        # print("hit exception")
        # Handle exceptions by displaying an error message to the user
        helper.throw_exception(e, message, bot, logging)
