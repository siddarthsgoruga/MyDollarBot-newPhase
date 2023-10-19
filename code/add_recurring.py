import helper # Import the helper module for utility functions
import logging # Import the logging module for error handling
from telebot import types # Import types module from the telebot library for user interface
from datetime import datetime # Import datetime module for date and time handling
from dateutil.relativedelta import relativedelta


option = {} # A dictionary to store temporary user options

# Define a function to start the expense recording process
def run(message, bot):

    # Read the JSON file to retrieve existing spending data
    helper.read_json()
    chat_id = message.chat.id # Get the unique chat ID for the current user
    
    # Remove any previous temporary choices for the user
    option.pop(chat_id, None)  

    # Create a keyboard markup for displaying spending categories to the user
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2

    # Add spending categories to the keyboard for user selection
    for c in helper.getSpendCategories():
        markup.add(c)
    
    # Ask the user to select a category or cancel the operation
    msg = bot.reply_to(message, 'Select Category or Select Cancel to cancel the operation', reply_markup=markup)
    
    # Register the next step handler to process the user's choice
    bot.register_next_step_handler(msg, post_category_selection, bot)

# Define a function to handle the user's selected spending category
def post_category_selection(message, bot):
    try:
        chat_id = message.chat.id
        selected_category = message.text

        # Check if the selected category is valid
        if selected_category not in helper.getSpendCategories():
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this category \"{}\"!".format(selected_category))
        
        if selected_category != "Cancel":
            option[chat_id] = selected_category # Store the selected category in the user's options
            
            # Ask the user to enter the expense amount or cancel the operation
            message = bot.send_message(chat_id, 'How much did you spend on {}? \n(Enter numeric values only) or enter Cancel to cancel the operation'.format(str(option[chat_id])))
            
            # Register the next step handler to process the user's entered amount
            bot.register_next_step_handler(message, post_amount_input, bot, selected_category)
        else:
            text_intro = "Cancelled the operation.\nSelect "
            
            # Generate a list of available commands
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            
            # Send a message to the user with available commands
            bot.send_message(chat_id, text_intro)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))
        
        # Generate a display text with available menu options
        display_text = ""
        commands = helper.getCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        
        # Ask the user to select a menu option from the available choices
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)

# Define a function to handle the user's entered expense amount
def post_amount_input(message, bot, selected_category):
    try:
        chat_id = message.chat.id
        amount_entered = message.text

        # Check if the user canceled the operation
        if amount_entered != "Cancel":
            # Validate and convert the entered amount to a numeric value
            amount_value = helper.validate_entered_amount(amount_entered)  # validate
            
            # Ensure that the amount is not zero
            if amount_value == 0:  # cannot be $0 spending
                raise Exception("Spent amount has to be a non-zero number.")
            
            # Ask the user to enter the expense amount or cancel the operation
            message = bot.send_message(chat_id, 'For how many months in the future will the expense be there? \n(Enter integer values only) or enter Cancel to cancel the operation'.format(str(option[chat_id])))
            
             # Register the next step handler to process the user's entered amount
            bot.register_next_step_handler(message, post_duration_input, bot, selected_category, amount_value)
        else :
            text_intro = "Cancelled the operation.\nSelect "

            # Generate a display text with available menu options
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            
            # Ask the user to select a menu option from the available choices
            bot.send_message(chat_id, text_intro)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))

# Define a function to handle the user's entered expense amount
def post_duration_input(message, bot, selected_category, amount_value):
    try:
        chat_id = message.chat.id
        duration_entered = message.text

        # Check if the user canceled the operation
        if duration_entered != 'Cancel':
            # Validate and convert the entered amount to a numeric value
            duration_value = helper.validate_entered_duration(duration_entered)
            
            # Ensure that the amount is not zero
            if duration_value == 0:
                raise Exception("Duration has to be a non-zero integer.")
                    
            for i in range(int(duration_value)):
                # Get the current date and time for the expense entry
                date_of_entry = (datetime.today() + relativedelta(months=+i)).strftime(helper.getDateFormat() + ' ' + helper.getTimeFormat())
                date_str, category_str, amount_str = str(date_of_entry), str(option[chat_id]), str(amount_value)
                
                # Add the user's expenditure record to the JSON data
                helper.write_json(add_user_record(chat_id, "{},{},{}".format(date_str, category_str, amount_str)))
            
            # Inform the user that the expense has been recorded
            bot.send_message(chat_id, 'The following expenditure has been recorded: You have spent ${} for {} for the next {} months'.format(amount_str, category_str, duration_value))
        else :
            text_intro = "Cancelled the operation.\nSelect "

            # Generate a list of available exit commands
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            
            # Send a message to the user with available commands
            bot.send_message(chat_id, text_intro)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))

# Define a function to add the user's expenditure record
def add_user_record(chat_id, record_to_be_added):
    # Read the existing user data from the JSON file
    user_list = helper.read_json()
    
    # Check if the user's data exists, and create a new record if not
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()

    # Append the new record to the user's data
    user_list[str(chat_id)]['data'].append(record_to_be_added)
    return user_list
