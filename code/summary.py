import history_summary
import logging
from summarize import PDF
import display_summary
import estimate_summary
import display_Asc

def run(message, bot):
    try:
        history=[]
        chat_id = message.chat.id
        data=history_summary.run(message,bot)
        print(data)
        if(data==['No Spending records']):
            bot.send_message(chat_id,"There are No spenging records. Please add your spendings")
            return
        history=data[0]
        history_text = '\n'.join(history)
        history_graph=data[1]
        #print(history_text)
        #print(history_graph)
        bot.send_message(chat_id, "The PDF is getting ready. Please Wait!")
        pdf = PDF()
        pdf.add_page()
        pdf.chapter_body(history_text,history_graph)
        display_data=display_summary.run(message,bot)
        data= display_data[0]
        #print(data)
        data_image= display_data[1]
        #print(data_image)
        #for i in data_image:
        #    bot.send_photo(chat_id, photo=open(i, 'rb'))
        #for i in data:
            #i= '\n'.join(i)
            #print(i)
        
        pdf.chapter_displaybody(data,data_image)
        
        data_estimate=estimate_summary.run(message,bot)
        #print(data_estimate,"this is summary.run")
        data_day = data_estimate[0]
        data_month = data_estimate[1]
        #print(data_day,data_day,"this is summary.run")
        pdf.chapter_estimatebody(data_day,data_month)

        data_sorted = display_Asc.run(message,bot)
        print(data_sorted,"this is data_sorted")
        data_order=[]
        
        data_order.append(data_sorted[0])
        data_order.append(data_sorted[1])
        print(data_order)

        pdf.chapter_asc_descbody(data_order[0],data_order[1])
        pdf.output("spending_history_beautified.pdf",'F')
        #print("******the ouput pdf for history is already created and now trying the display_summary functions")
        
        #pdf.output("new.pdf")
        bot.send_message(chat_id, "Here is your spending report !")
        bot.send_document(chat_id, document=open('spending_history_beautified.pdf', 'rb'))

    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, "Oops!" + str(e))