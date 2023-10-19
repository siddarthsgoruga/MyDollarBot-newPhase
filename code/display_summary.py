# Import necessary modules and libraries
import time
import os
import helper
import graphing_for_day
import graphing_for_month
import logging
from telebot import types
from datetime import datetime

"""
    Main function to run the display of total spending and corresponding plots.
    :param message: Message object from the user.
    :param bot: Telegram bot instance.
    """
def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id

    # Retrieve user's spending history
    history = helper.getUserHistory(chat_id)

    # Check if there is no history data
    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        # Call the function to display total spendings
        display_total(message, bot)
        return data,data_image

total_day="" # Initialize the total spending for the day
total_month="" # Initialize the total spending for the month
bud="" # Initialize budget data
data=[] # List to store spending data text
data_image=[] # List to store image filenames

def display_total(message, bot):
    """
    Display total spendings and generate plots.
    :param message: Message object from the user.
    :param bot: Telegram bot instance.
    """
    
    global total_day
    global total_month
    global bud
    try:
        chat_id = message.chat.id
        DayWeekMonth = message.text
        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")
        total_text_day = ""
        total_text_month = ""
        budgetData = {}

         # Determine the budget data based on the user's configuration
        if helper.isOverallBudgetAvailable(chat_id):
            budgetData = helper.getOverallBudget(chat_id)
        elif helper.isCategoryBudgetAvailable(chat_id):
            budgetData = helper.getCategoryBudget(chat_id)

        # Query for the current day and month
        query_day = datetime.now().today().strftime(helper.getDateFormat())
        query_dayResult = [value for index, value in enumerate(history) if str(query_day) in value]
        query_month = datetime.now().today().strftime(helper.getMonthFormat())
        query_monthResult = [value for index, value in enumerate(history) if str(query_month) in value]

        # Calculate total spendings for the day and month
        total_text_day = calculate_spendings(query_dayResult)
        total_text_month = calculate_spendings(query_monthResult)

        total_day = total_text_day
        total_month = total_text_month
        bud= budgetData

        # Display total spending text for the day
        spending_text_day = display_budget_by_text(history, budgetData)
        spending_text_month = display_budget_by_text(history, budgetData)
        if len(total_text_day) == 0:
            spending_text_day += "\nYou have no spendings for {}!".format('of the day'.lower())
            bot.send_message(chat_id, spending_text_day)
            data.append(spending_text_day)

        else:
            spending_text_day += "\nHere are your total spendings {}:\nCATEGORIES, AMOUNT \n{}".format(
                'of the day'.lower(), total_text_day)
            data.append(spending_text_day)
            

        # Display total spending text for the month
        if len(total_text_month) == 0:
            spending_text_month += "\nYou have no spendings for {}!".format('of the month'.lower())
            bot.send_message(chat_id, spending_text_month)
            data.append(spending_text_month)

        else:
            spending_text_month += "\nHere are your total spendings {}:\nCATEGORIES, AMOUNT \n{}".format(
            'of the month'.lower(), total_text_month)
        data.append(spending_text_month)

        # Generate and send plots
        plot_total(message,bot)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))

def plot_total(message, bot):
    """
    Generate and send plots for total spendings.
    :param message: Message object from the user.
    :param bot: Telegram bot instance.
    """
    chat_id = message.chat.id

    # Generate and send plots for the day
    graphing_for_day.visualize(total_day,bud)
    data_image.append('expenditure_day.png')
    #os.remove('expenditure.png')
    print("************Sent the photo 1 to the chat for day")
    graphing_for_day.viz(total_day)
    data_image.append('expend_day.png')
    #os.remove('expend.png')
    graphing_for_day.vis(total_day)
    data_image.append('pie_day.png')
    #os.remove('pie.png')

    # Generate and send plots for the month
    graphing_for_month.visualize(total_month,bud)
    graphing_for_month.visualize(total_month,bud)
    data_image.append('expenditure_month.png')
    #os.remove('expenditure.png')

    graphing_for_month.viz(total_month)
    data_image.append('expend_month.png')
    #os.remove('expend.png')

    graphing_for_month.vis(total_month)
    data_image.append('pie_month.png')
    #os.remove('pie.png')

def calculate_spendings(queryResult):
    """
    Calculate total spendings from the query result.
    :param queryResult: List of spending history data.
    :return: Total spending text.
    """
    total_dict = {}

    for row in queryResult:
        # Split the row into date, category, and amount
        s = row.split(',')
        # Category
        cat = s[1]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
    total_text = ""
    for key, value in total_dict.items():
        total_text += str(key) + " $" + str(value) + "\n"
    return total_text


def calculate_spendings_acs(queryResult):
    sorted_data = sorted(queryResult, key=lambda x: float(x.split(',')[2]))
    print("entered")
    print(sorted_data)

def calculate_spendings_desc(queryResult):
    sorted_data = sorted(queryResult, key=lambda x: float(x.split(',')[2]), reverse=True)
    print("entered")
    print(sorted_data)

def display_budget_by_text(history, budget_data) -> str:
    query = datetime.now().today().strftime(helper.getMonthFormat())
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
        budget_display += "Overall Budget is: " + str(budget_val) + "\n____________________\nCurrent remaining budget is " + str(
            remaining) 
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
        budget_display += "______________________\nCurrent remaining budget is: \n"
        # show the remaining budgets
        for key in categ_remaining.keys():
            budget_display += key + ":" + str(categ_remaining[key]) + "\n"
    return budget_display