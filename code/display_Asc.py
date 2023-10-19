import helper
import logging

from telebot import types


def run(message,bot):
    #print("***********entered displayAcs run")
    helper.read_json()
    chat_id = message.chat.id
    history = helper.getUserHistory(chat_id)
    #print("***********got history")
    if history is None:
        bot.send_message(chat_id, "Sorry, there are no records of the spending!")
    else:
        #print("***********calling the display_total function")
        #print("************called the display_total func")
        display_total(message, bot)
        return data
    
#bud=""
data=[]
def display_total(message,bot):
    try:
        #print("**************entered display total funct")
        chat_id = message.chat.id
        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")
        #budgetData = {}
        #if helper.isOverallBudgetAvailable(chat_id):
        #    budgetData = helper.getOverallBudget(chat_id)
        #elif helper.isCategoryBudgetAvailable(chat_id):
        #    budgetData = helper.getCategoryBudget(chat_id)
        
        query_acs= [value for index, value in enumerate(history)]
        queryResult_acs=calculate_spendings_acs(query_acs)

        query_desc= [value for index, value in enumerate(history)]
        queryResult_desc=calculate_spendings_desc(query_desc)
        #print(len(queryResult_acs))
        
        #bud= budgetData
        #spending_text_asc = display_budget_by_text(history, budgetData)
        #spending_text_desc = display_budget_by_text(history, budgetData)
        spending_text_asc =""
        spending_text_desc =""
        if len(queryResult_acs) == 0:
            spending_text_asc += "\nYou have no spendings!"
            bot.send_message(chat_id, spending_text_asc)
            data.append(spending_text_asc)

        else:
            spending_text_asc += "\nHere are your total spendings in Ascending Order:\nDATE & TIME, CATEGORIES, AMOUNT \n"
            for row in queryResult_acs:
                #print(row,"this is row")
                s = row.split(',')
                #print(s,"this is s")
                spending_text_asc += "\n {}, {}, {}".format(s[0],s[1],s[2])
            
            #bot.send_message(chat_id, spending_text_day)
            data.append(spending_text_asc)
            #print(spending_text_asc,"this is spending_text_asc")
            #print(data)

        if len(queryResult_desc) == 0:
            spending_text_desc += "\nYou have no spendings!"
            bot.send_message(chat_id, spending_text_desc)
            data.append(spending_text_desc)

        else:
            spending_text_desc += "\nHere are your total spendings in Descending Order:\nDATE & TIME, CATEGORIES, AMOUNT \n"
            for row in queryResult_desc:
                s = row.split(',')
                
                spending_text_desc += "\n {}, {}, {}".format(s[0],s[1],s[2])
            
            #bot.send_message(chat_id, spending_text_day)
            data.append(spending_text_desc)
            #print(spending_text_desc,"this is spending_text_desc")
            #print(data)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, str(e))
        
        
def calculate_spendings_acs(queryResult):
    sorted_data = sorted(queryResult, key=lambda x: float(x.split(',')[2]))
    #print("entered")
    #print(sorted_data)
    return sorted_data

def calculate_spendings_desc(queryResult):
    sorted_data = sorted(queryResult, key=lambda x: float(x.split(',')[2]), reverse=True)
    #print("entered")
    #print(sorted_data)
    return sorted_data

