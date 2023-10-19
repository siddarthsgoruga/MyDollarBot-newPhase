import helper
import logging

# Define a function to display the user's budget
def run(message, bot):
    try:
        chat_id = message.chat.id

        # Check if an overall budget is available for the user
        if helper.isOverallBudgetAvailable(chat_id):
            display_overall_budget(message, bot)
        
        # Check if a category budget is available for the user
        elif helper.isCategoryBudgetAvailable(chat_id):
            display_category_budget(message, bot)
        else:
            raise Exception('Budget does not exist. Use ' + helper.getOptions()['update'] + ' option to add/update the budget')
    except Exception as e:
        # Handle exceptions and log errors
        helper.throw_exception(e, message, bot, logging)

# Function to display the overall budget
def display_overall_budget(message, bot):
    chat_id = message.chat.id
    data = helper.getOverallBudget(chat_id)
    bot.send_message(chat_id, 'Overall Budget: $' + data)

# Function to display the category budget
def display_category_budget(message, bot):
    chat_id = message.chat.id
    data = helper.getCategoryBudget(chat_id)
    res = "Budget Summary\n"
    for c, v in data.items():
        res = res + c + ": $" + v + "\n"
    bot.send_message(chat_id, res)
