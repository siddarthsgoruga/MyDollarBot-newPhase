# Import necessary modules and libraries
import time
import os
import helper
import graphing
import logging
from telebot import types
from datetime import datetime


def run(message, bot):
    # Read user data from JSON file
    helper.read_json()
    chat_id = message.chat.id

    # Get the user's expense history
    history = helper.getUserHistory(chat_id)
    
    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        # Create a reply keyboard with display options
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for mode in helper.getSpendDisplayOptions():
            markup.add(mode)
        
        # Prompt the user to select a display option
        msg = bot.reply_to(message, 'Please select a category to see details or Select Cancel to cancel the operation', reply_markup=markup)
        bot.register_next_step_handler(msg, display_total, bot)

# Initialize variables to store total spending and budget data
total=""
bud=""

# Function to display total expenditure
def display_total(message, bot):
    global total
    global bud
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text

        if DayWeekMonth not in helper.getSpendDisplayOptions():
            raise Exception("Invalid operation\"{}\"!Please try again by choosing a valid option".format(DayWeekMonth))
        if DayWeekMonth != "Cancel":
            history = helper.getUserHistory(chat_id)
            if history is None:
                raise Exception("Oops! Looks like you do not have any spending records!")

            # Send a typing indicator to let the user know the bot is processing
            bot.send_message(chat_id, "Hold on! Calculating...")
            bot.send_chat_action(chat_id, 'typing')
            time.sleep(0.5)
            total_text = ""

            # Create a query to filter expense history based on the selected display option
            budgetData = {}
            if helper.isOverallBudgetAvailable(chat_id):
                budgetData = helper.getOverallBudget(chat_id)
            elif helper.isCategoryBudgetAvailable(chat_id):
                budgetData = helper.getCategoryBudget(chat_id)

            if DayWeekMonth == 'Day':
                query = datetime.now().today().strftime(helper.getDateFormat())

                # query all that contains today's date
                queryResult = [value for index, value in enumerate(history) if str(query) in value]
                print(queryResult,"this is display")
            elif DayWeekMonth == 'Month':
                query = datetime.now().today().strftime(helper.getMonthFormat())
                # query all that contains today's date
                queryResult = [value for index, value in enumerate(history) if str(query) in value]

            # Calculate total spending and store it in 'total_text'
            total_text = calculate_spendings(queryResult)
            total=total_text
            bud=budgetData

            # Generate a text representation of the total spending
            spending_text = display_budget_by_text(history, budgetData)
            if len(total_text) == 0:
                spending_text += "----------------------\nYou have no spendings for {}!".format(DayWeekMonth)
                bot.send_message(chat_id, spending_text)
            else:
                spending_text += "\n----------------------\nHere are your total spendings {}:\nCATEGORIES,AMOUNT \n----------------------\n{}".format(
                    DayWeekMonth.lower(), total_text)
                bot.send_message(chat_id, spending_text)
                
                # Create a reply keyboard with plot options
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row_width = 2
                for plot in helper.getplot():
                    markup.add(plot)
                
                # Prompt the user to select a plot option
                msg = bot.reply_to(message, 'Please select a plot to see the total expense or Type Cancel to cancel the operation', reply_markup=markup)
                bot.register_next_step_handler(msg, plot_total, bot)
            


        else:
            # If the user cancels the operation, send a cancellation message
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(chat_id, text_intro)

        
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))

# Function to plot total spending
def plot_total(message, bot):
    chat_id = message.chat.id
    pyi=message.text
    if pyi == 'Bar with budget':
       # Generate a bar chart with budget data
       graphing.visualize(total,bud)
       bot.send_photo(chat_id, photo=open('expenditure.png', 'rb'))
       os.remove('expenditure.png')
    elif pyi == 'Bar without budget': 
       # Generate a bar chart without budget data
       graphing.viz(total)
       bot.send_photo(chat_id, photo=open('expend.png', 'rb'))
       os.remove('expend.png')
    elif pyi == 'Pie':
       # Generate a pie chart
       graphing.vis(total)
       bot.send_photo(chat_id, photo=open('pie.png', 'rb'))
       os.remove('pie.png')
    elif pyi == 'Cancel':
        text_intro = "Cancelled the operation.\nSelect "
        commands = helper.getExitCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            text_intro += "/" + c + " to "
            text_intro += commands[c] + "\n\n"
        bot.send_message(chat_id, text_intro)
    else:
          bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
          raise Exception("Sorry I don't recognise this plot type \"{}\"!".format(pyi))
def calculate_spendings(queryResult):
    total_dict = {}

    for row in queryResult:
        #print(row,"this is calculate")
        # date,cat,money
        s = row.split(',')
        # cat
        cat = s[1]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        total_text += str(key) + " $" + str(value) + "\n"
    print(total_text)
    return total_text




def display_budget_by_text(history, budget_data) -> str:
    query = datetime.now().today().strftime(helper.getMonthFormat())
    # query all expense history that contains today's date
    queryResult = [value for index, value in enumerate(history) if str(query) in value]
    total_text = calculate_spendings(queryResult)
    budget_display = ""
    total_text_split = [line for line in total_text.split('\n') if line.strip() != '']

    if isinstance(budget_data, str):
        # if budget is string denoting it is overall budget
        budget_val = float(budget_data)
        total_expense = 0
        # sum all expense
        for expense in total_text_split:
            a = expense.split(' ')
            amount = a[1].replace("$", "")
            total_expense += float(amount)
        # calculate the remaining budget
        remaining = budget_val - total_expense
        # set the return message
        budget_display += "Overall Budget is: " + str(budget_val) + "\n----------------------\nCurrent remaining budget is " + str(
            remaining) + "\n"
    elif isinstance(budget_data, dict):
        budget_display += "Budget by Catergories is:\n"
        categ_remaining = {}
        # categorize the budgets by their categories
        for key in budget_data.keys():
            budget_display += key + ":" + budget_data[key] + "\n"
            categ_remaining[key] = float(budget_data[key])
        #  calculate the remaining budgets by categories
        for i in total_text_split:
            # the expense text is in the format like "Food $100"
            a = i.split(' ')
            a[1] = a[1].replace("$", "")
            categ_remaining[a[0]] = categ_remaining[a[0]] - float(a[1]) if a[0] in categ_remaining else -float(a[1])
        budget_display += "----------------------\nCurrent remaining budget is: \n"
        # show the remaining budgets
        for key in categ_remaining.keys():
            budget_display += key + ":" + str(categ_remaining[key]) + "\n"
    return budget_display
