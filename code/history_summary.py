import helper
import logging
import matplotlib.pyplot as plt



def run(message,bot):
    try:
        pdfspend_history=[]
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        spend_total_str = ""
        amount=0.0
        am=""
        Dict = {'Jan': 0.0,'Feb': 0.0,'Mar': 0.0,'Apr': 0.0,'May': 0.0, 'Jun': 0.0, 'Jul': 0.0,'Aug': 0.0, 'Sep': 0.0, 'Oct': 0.0, 'Nov': 0.0, 'Dec': 0.0}
        if user_history is None:
            spend_total_str="No Spending records"
            pdfspend_history.append(spend_total_str)
            
            return pdfspend_history
        spend_total_str = "Here is your spending history : \n_________________\nDATE, CATEGORY, AMOUNT\n"
        if len(user_history) == 0:
            spend_total_str="No Spending records"
            pdfspend_history.append(spend_total_str)
            return pdfspend_history
        else:
            for rec in user_history:
                spend_total_str += str(rec) + "\n"
                av=str(rec).split(",")
                ax=av[0].split("-")
                am=ax[1]
                amount=Dict[am]+ float(av[2])
                Dict[am]=amount
        pdfspend_history.append(spend_total_str)
        plt.clf()
        width=1.0
        plt.bar(Dict.keys(), Dict.values(), width, color='g')
        plt.savefig('histo.png')
        return pdfspend_history, 'histo.png'
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops!" + str(e))


import helper
import logging
import matplotlib.pyplot as plt



def run(message,bot):
    try:
        pdfspend_history=[]
        helper.read_json()
        chat_id = message.chat.id
        user_history = helper.getUserHistory(chat_id)
        spend_total_str = ""
        amount=0.0
        am=""
        Dict = {'Jan': 0.0,'Feb': 0.0,'Mar': 0.0,'Apr': 0.0,'May': 0.0, 'Jun': 0.0, 'Jul': 0.0,'Aug': 0.0, 'Sep': 0.0, 'Oct': 0.0, 'Nov': 0.0, 'Dec': 0.0}
        if user_history is None:
            spend_total_str="No Spending records"
            pdfspend_history.append(spend_total_str)            
            return pdfspend_history
        spend_total_str = "Here is your spending history : \n_________________\nDATE, CATEGORY, AMOUNT\n"
        if len(user_history) == 0:
            spend_total_str="No Spending records"
            pdfspend_history.append(spend_total_str)
            return pdfspend_history
        else:
            for rec in user_history:
                spend_total_str += str(rec) + "\n"
                av=str(rec).split(",")
                ax=av[0].split("-")
                am=ax[1]
                amount=Dict[am]+ float(av[2])
                Dict[am]=amount
        pdfspend_history.append(spend_total_str)
        plt.clf()
        width=1.0
        plt.bar(Dict.keys(), Dict.values(), width, color='g')
        plt.savefig('histo.png')
        return pdfspend_history, 'histo.png'
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops!" + str(e))


