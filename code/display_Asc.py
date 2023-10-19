import helper
import logging
from telebot import types


def run(message,bot):
    helper.read_json() # Read user data from JSON
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        # Call the function to display total spendings
        display_total(message, bot)
        return data

data=[]

# Function to display total spendings
def display_total(message,bot):
    try:
        chat_id = message.chat.id
        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")
        
         # Create two sets of data, ascending and descending
        query_acs= [value for index, value in enumerate(history)]
        queryResult_acs=calculate_spendings_acs(query_acs)

        query_desc= [value for index, value in enumerate(history)]
        queryResult_desc=calculate_spendings_desc(query_desc)
        
        spending_text_asc =""
        spending_text_desc =""
        if len(queryResult_acs) == 0:
            spending_text_asc += "\nYou have no spendings!"
            bot.send_message(chat_id, spending_text_asc)
            data.append(spending_text_asc)

        else:
            spending_text_asc += "\nHere are your total spendings in Ascending Order:\nDATE & TIME, CATEGORIES, AMOUNT \n"
            for row in queryResult_acs:
                s = row.split(',')
                spending_text_asc += "\n {}, {}, {}".format(s[0],s[1],s[2])
            
            data.append(spending_text_asc)

        if len(queryResult_desc) == 0:
            spending_text_desc += "\nYou have no spendings!"
            bot.send_message(chat_id, spending_text_desc)
            data.append(spending_text_desc)

        else:
            spending_text_desc += "\nHere are your total spendings in Descending Order:\nDATE & TIME, CATEGORIES, AMOUNT \n"
            for row in queryResult_desc:
                s = row.split(',')
                
                spending_text_desc += "\n {}, {}, {}".format(s[0],s[1],s[2])
            
            data.append(spending_text_desc)
            
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))
        
# Function to calculate total spendings in ascending order        
def calculate_spendings_acs(queryResult):
    sorted_data = sorted(queryResult, key=lambda x: float(x.split(',')[2]))
    return sorted_data

# Function to calculate total spendings in descending order
def calculate_spendings_desc(queryResult):
    sorted_data = sorted(queryResult, key=lambda x: float(x.split(',')[2]), reverse=True)
    return sorted_data

