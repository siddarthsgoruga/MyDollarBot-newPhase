import helper # Import the helper module for utility functions
import logging # Import the logging module for error handling
from telebot import types  # Import the 'types' module from the 'telebot' library


# Define a function to update the overall or category budget
def run(message, bot):
    chat_id = message.chat.id # Get the chat ID from the message
    
    # Check if an overall budget is available for the user
    if helper.isOverallBudgetAvailable(chat_id):
        update_overall_budget(chat_id, bot)
    
    # Check if a category budget is available for the user
    elif helper.isCategoryBudgetAvailable(chat_id):
        update_category_budget(message, bot)
    else:
        # If no budget is available, prompt the user to select a budget type
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        options = helper.getBudgetTypes()
        markup.row_width = 2
        for c in options.values():
            markup.add(c)
        msg = bot.reply_to(message, 'Select Budget Type or Select Cancel to cancel the operation', reply_markup=markup)
        bot.register_next_step_handler(msg, post_type_selection, bot)

# Function to handle the user's budget type selection
def post_type_selection(message, bot):
    try:
        chat_id = message.chat.id
        op = message.text
        options = helper.getBudgetTypes()

        # Check if the selected option is valid
        if op not in options.values():
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this operation \"{}\"!".format(op))
            
        if op == options['overall']:
            update_overall_budget(chat_id, bot)
        elif op == options['category']:
            update_category_budget(message, bot)
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
        helper.throw_exception(e, message, bot, logging)

# Function to update the overall budget
def update_overall_budget(chat_id, bot):
    if (helper.isOverallBudgetAvailable(chat_id)):
        currentBudget = helper.getOverallBudget(chat_id)
        msg_string = 'Current Budget is ${}\n\nEnter your new monthly budget (Enter numeric values only) or Enter Cancel to cancel the operation \n'
        message = bot.send_message(chat_id, msg_string.format(currentBudget))
    else:
        message = bot.send_message(chat_id, 'Enter your monthly budget (Enter numeric values only)or Enter Cancel to cancel the operation \n')
    bot.register_next_step_handler(message, post_overall_amount_input, bot)


# Function to handle the user's input for the overall budget amount
def post_overall_amount_input(message, bot):
    try:
        chat_id = message.chat.id

        if message.text != "Cancel":
            amount_value = helper.validate_entered_amount(message.text)
            total_income = helper.getTotalIncome(chat_id)

            if total_income is not None and float(amount_value) > float(total_income):
                budget_deficit = float(amount_value) - float(total_income)
                alert_message = f"⚠️\uFE0F Your budget exceeds your total income by ${budget_deficit:.2f} " + "\n(Do you want to update your budget)"
    
                # Define markup here before using it
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                options = helper.getYesNoOptions().values()
                markup.row_width = 2
                for c in options:
                    markup.add(c)
                
                bot.send_message(chat_id, alert_message, reply_markup=markup)
                msg = bot.reply_to(message, 'Select Option', reply_markup=markup)
                bot.register_next_step_handler(msg, post__selection, bot, amount_value)
        
            else :
                update_overall_budget_amount(message, amount_value, bot)

        else:
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(chat_id, text_intro)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)

# Function to handle the user's yes/no selection after budget alert
def post__selection(message, bot, amount_val ) :
    chat_id = message.chat.id
    selected_option = message.text
    options = helper.getYesNoOptions()
    if selected_option == options['yes']:
        update_overall_budget_amount(message, amount_val, bot)
    else :
        update_overall_budget(chat_id, bot)

# Function to update the overall budget amount
def update_overall_budget_amount(message, amount_value, bot) :
    chat_id = message.chat.id
    if amount_value == 0:
        raise Exception("Invalid amount.")
    user_list = helper.read_json()
    if str(chat_id) not in user_list:
            user_list[str(chat_id)] = helper.createNewUserRecord()
    user_list[str(chat_id)]['budget']['overall'] = amount_value
    helper.write_json(user_list)
    bot.send_message(chat_id, 'Budget Updated!')

# Function to update the category budget
def update_category_budget(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    categories = helper.getSpendCategories()
    markup.row_width = 2
    for c in categories:
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category or Select Cancel to cancel the operation', reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)


# Function to handle the user's category selection
def post_category_selection(message, bot):
    try:
        chat_id = message.chat.id
        selected_category = message.text
        categories = helper.getSpendCategories()
        if selected_category not in categories:
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this category \"{}\"!".format(selected_category))
        if selected_category != "Cancel":
            if helper.isCategoryBudgetByCategoryAvailable(chat_id, selected_category):
                currentBudget = helper.getCategoryBudgetByCategory(chat_id, selected_category)
                msg_string = 'Current monthly budget for {} is {}\n\nEnter your new monthly budget for {} (Enter numeric values only) or Enter Cancel to cancel the operation\n'
                message = bot.send_message(chat_id, msg_string.format(selected_category, currentBudget, selected_category))
            else:
                message = bot.send_message(chat_id, 'Enter monthly budget for ' + selected_category + '(Enter numeric values only) or Enter Cancel to cancel the operation\n')
            bot.register_next_step_handler(message, post_category_amount_input, bot, selected_category)
        else:
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(chat_id, text_intro)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def post_category_amount_input(message, bot, category):
    try:
        chat_id = message.chat.id
        if message.text != 'Cancel':
            amount_value = helper.validate_entered_amount(message.text)
            data = helper.getCategoryBudget(chat_id)
            categ_sum = 0.0
            if data is not None and category in data :
                categ_sum = float(data[category]) 
            
            category_total = sum(float(value) for value in data.values()) if data is not None else 0.0
            total_sum = category_total + float(amount_value) - categ_sum
            total_income = float(helper.getTotalIncome(chat_id))

            if total_income is not None and total_sum > total_income:
                budget_deficit = total_sum - total_income
                alert_message = f"⚠️\uFE0F Your total budget exceeds your total income by ${budget_deficit:.2f} " + "\n(Do you want to update your budget)"
    
                # Define markup here before using it
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                options = helper.getYesNoOptions().values()
                markup.row_width = 2
                for c in options:
                    markup.add(c)
                
                bot.send_message(chat_id, alert_message, reply_markup=markup)
                msg = bot.reply_to(message, 'Select Option', reply_markup=markup)
                bot.register_next_step_handler(msg, post_yesno_selection, bot, amount_value, category)
            else :
                update_category_budget_amount(chat_id, bot, amount_value, category)
      
        else :
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(chat_id, text_intro)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)


def post_yesno_selection(message, bot, amount_val, category ) :
    chat_id = message.chat.id
    selected_option = message.text
    options = helper.getYesNoOptions()
    if selected_option == options['yes']:
        update_category_budget_amount( chat_id, bot, amount_val, category)
    else :
        update_category_budget(message, bot)


def update_category_budget_amount(chat_id, bot, amount_val, category) :
    if amount_val == 0:
            raise Exception("Invalid amount.")
    user_list = helper.read_json()
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.createNewUserRecord()
    if user_list[str(chat_id)]['budget']['category'] is None:
        user_list[str(chat_id)]['budget']['category'] = {}
    user_list[str(chat_id)]['budget']['category'][category] = amount_val
    helper.write_json(user_list)
    message = bot.send_message(chat_id, 'Budget for ' + category + ' Created!')
    post_category_add(message, bot)


def post_category_add(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getUpdateOptions().values()
    markup.row_width = 2
    for c in options:
        markup.add(c)
    msg = bot.reply_to(message, 'Select Option', reply_markup=markup)
    bot.register_next_step_handler(msg, post_option_selection, bot)


def post_option_selection(message, bot):
    selected_option = message.text
    options = helper.getUpdateOptions()
    if selected_option == options['continue']:
        update_category_budget(message, bot)
