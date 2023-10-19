from distutils.command.install_egg_info import to_filename
import time
import helper
import logging
from telebot import types



def run(message, bot):
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    if history is None:
        bot.send_message(
            chat_id, "Oops! Looks like you do not have any spending records!")
    else:
        return(estimate_total(message,bot))

        

def estimate_total(message, bot):
    data_estimate_day=[]
    data_estimate_month=[]
    chat_id = message.chat.id
    DayWeekMonth = message.text
    try:
        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception(
                "Oops! Looks like you do not have any spending records!")

        

        days_to_estimate_day=1
        days_to_estimate_month=30
        
            # query all that contains today's date
        # query all that contains all history
        queryResult = [value for index, value in enumerate(history)]
        print(queryResult)
        total_text_day = calculate_estimate(queryResult, days_to_estimate_day)
        total_text_month = calculate_estimate(queryResult, days_to_estimate_month)

        spending_text_day = ""
        spending_text_month= ""
        if len(total_text_day) == 0:
            spending_text_day = "You have no estimate for {}!".format(DayWeekMonth)
        else:
            spending_text_day = "\nHere are your estimated spendings for the day :"
            spending_text_day += "\n_____________________________________________\nCATEGORIES,AMOUNT \n"
            spending_text_day += total_text_day


        if len(total_text_month) == 0:
            spending_text_month = "You have no estimate for {}!".format(DayWeekMonth)
        else:
            spending_text_month = "Here are your estimated spendings for the month :"
            spending_text_month += "\n_____________________________________________\nCATEGORIES,AMOUNT \n"
            spending_text_month += total_text_month
            

        #bot.send_message(chat_id, spending_text_day)
        #bot.send_message(chat_id, spending_text_month)
        
        data_estimate_day=[spending_text_day]
        data_estimate_month=[spending_text_month]
        return (data_estimate_day,data_estimate_month)
    
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))
        
    
    

def calculate_estimate(queryResult, days_to_estimate):
    total_dict = {}
    days_data_available = {}
    for row in queryResult:
        # date,cat,money
        s = row.split(',')
        # cat
        cat = s[1]
        date_str = s[0][0:11]
        if cat in total_dict:
            # round up to 2 decimal
            total_dict[cat] = round(total_dict[cat] + float(s[2]), 2)
        else:
            total_dict[cat] = float(s[2])
        if date_str not in days_data_available:
            days_data_available[date_str] = True

    total_text = ""
    for key, value in total_dict.items():
        category_count = len(days_data_available)
        daily_avg = value / category_count
        estimated_avg = round(daily_avg * days_to_estimate, 2)
        total_text += str(key) + " $" + str(estimated_avg) + "\n"
    return total_text