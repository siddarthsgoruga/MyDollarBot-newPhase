from distutils.command.install_egg_info import to_filename
import time
import helper
import logging
from telebot import types



def run(message, bot):
    # Read user data from JSON
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)

    # Check if the user has any spending records
    if history is None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!")
    else:
        # Call the estimate_total function to calculate and return estimated spendings
        return(estimate_total(message,bot))

        

def estimate_total(message, bot):
    data_estimate_day=[]  # List to store the estimated spending for the day
    data_estimate_month=[] # List to store the estimated spending for the month
    chat_id = message.chat.id
    DayWeekMonth = message.text
    try:
        history = helper.getUserHistory(chat_id)

        # Check if the user has any spending records
        if history is None:
            raise Exception(
                "Oops! Looks like you do not have any spending records!")

        
        # Define the number of days to estimate for the day and month
        days_to_estimate_day=1
        days_to_estimate_month=30
        
        # Query all spending records
        queryResult = [value for index, value in enumerate(history)]
        
        # Calculate estimated spending for the day and month
        total_text_day = calculate_estimate(queryResult, days_to_estimate_day)
        total_text_month = calculate_estimate(queryResult, days_to_estimate_month)

        spending_text_day = ""
        spending_text_month= ""

        # Prepare estimated spending text for the day
        if len(total_text_day) == 0:
            spending_text_day = "You have no estimate for {}!".format(DayWeekMonth)
        else:
            spending_text_day = "\nHere are your estimated spendings for the day :"
            spending_text_day += "\n_____________________________________________\nCATEGORIES,AMOUNT \n"
            spending_text_day += total_text_day

        # Prepare estimated spending text for the month
        if len(total_text_month) == 0:
            spending_text_month = "You have no estimate for {}!".format(DayWeekMonth)
        else:
            spending_text_month = "Here are your estimated spendings for the month :"
            spending_text_month += "\n_____________________________________________\nCATEGORIES,AMOUNT \n"
            spending_text_month += total_text_month
            
        # Populate the data_estimate_day and data_estimate_month lists
        data_estimate_day=[spending_text_day]
        data_estimate_month=[spending_text_month]

        # Return the estimated spending data
        return (data_estimate_day,data_estimate_month)
    
    except Exception as e:
        # Log exceptions and inform the user of any errors
        logging.exception(str(e))
        bot.reply_to(message, str(e))
        
    
    

def calculate_estimate(queryResult, days_to_estimate):
    total_dict = {} # Dictionary to store total spending per category
    days_data_available = {} # Dictionary to track data available days
    for row in queryResult:
        # Extract date, category, and amount from the row
        s = row.split(',')
        # category
        cat = s[1]
        date_str = s[0][0:11]

        # Calculate total spending per category
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])

        # Track available data days
        if date_str not in days_data_available:
            days_data_available[date_str] = True

    total_text = ""
    for key, value in total_dict.items():
        # Calculate daily average spending
        category_count = len(days_data_available)
        daily_avg = value / category_count

        # Estimate the total spending for the selected period
        estimated_avg = round(daily_avg * days_to_estimate, 2)
        total_text += str(key) + " $" + str(estimated_avg) + "\n"
    return total_text