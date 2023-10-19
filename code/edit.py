import re
import helper
import logging
from telebot import types


def run(m, bot):
    try :
        chat_id = m.chat.id
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2

        # Check if there are spending records for the user
        if helper.getUserHistory(chat_id) is None:
                raise Exception("Sorry! No spending records found!")
        
        # Check if user history is empty
        if helper.getUserHistory(chat_id) == 0:
                raise Exception("Sorry! No spending records found!")
        
        # Create a menu for selecting expenses to edit
        for c in helper.getUserHistory(chat_id):
            expense_data = c.split(',')
            str_date = "Date=" + expense_data[0]
            str_category = ",\t\tCategory=" + expense_data[1]
            str_amount = ",\t\tAmount=$" + expense_data[2]
            markup.add(str_date + str_category + str_amount)
        markup.add('Cancel')
        info = bot.reply_to(m, "Select expense to be edited or select Cancel to cancel the operation:", reply_markup=markup)
        bot.register_next_step_handler(info, select_category_to_be_updated, bot)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(m, "Oops! " + str(e))

def select_category_to_be_updated(m, bot):
    info = m.text
    if m.text != 'Cancel':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        selected_data = [] if info is None else info.split(',')
        for c in selected_data:
            markup.add(c.strip())
        markup.add('Cancel')
        choice = bot.reply_to(m, "Select what you want to update? or select Cancel to cancel the operation", reply_markup=markup)
        bot.register_next_step_handler(choice, enter_updated_data, bot, selected_data)
    else:
        text_intro = "Cancelled the operation.\nSelect "
        commands = helper.getExitCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            text_intro += "/" + c + " to "
            text_intro += commands[c] + "\n\n"
        bot.send_message(m.chat.id, text_intro)


def enter_updated_data(m, bot, selected_data):
    try :
        choice1 = "" if m.text is None else m.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row_width = 2
        for cat in helper.getSpendCategories():
            markup.add(cat)

        if 'Date' in choice1:
            new_date = bot.reply_to(m, "Please enter the new date (in dd-mmm-yyy format) or enter Cancel to cancel the operation")
            bot.register_next_step_handler(new_date, edit_date, bot, selected_data)

        elif 'Category' in choice1:
            new_cat = bot.reply_to(m, "Please select the new category or Cancel to cancel the operation", reply_markup=markup)
            bot.register_next_step_handler(new_cat, edit_cat, bot, selected_data)

        elif 'Amount' in choice1:
            new_cost = bot.reply_to(m, "Please type the new cost or Cancel to cancel the operation")
            bot.register_next_step_handler(new_cost, edit_cost, bot, selected_data)

        elif 'Cancel' in choice1:
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(m.chat.id, text_intro)
        else :
            bot.send_message(m.chat.id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this operation \"{}\"!".format(choice1))
    except Exception as e:
        # print("hit exception")
        helper.throw_exception(e, m, bot, logging)


def edit_date(m, bot, selected_data):
    user_list = helper.read_json()
    new_date = "" if m.text is None else m.text
    if new_date != 'Cancel' :
        date_format = r'^(([0][1-9])|([1-2][0-9])|([3][0-1]))\-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\-\d{4}$'
        x1 = re.search(date_format, new_date)
        if x1 is None:
            bot.reply_to(m, "The date is incorrect")
            return
        chat_id = m.chat.id
        data_edit = helper.getUserHistory(chat_id)
        for i in range(len(data_edit)):
            user_data = data_edit[i].split(',')
            selected_date = selected_data[0].split('=')[1]
            selected_category = selected_data[1].split('=')[1]
            selected_amount = selected_data[2].split('=')[1]
            if user_data[0] == selected_date and user_data[1] == selected_category and user_data[2] == selected_amount[1:]:
                data_edit[i] = new_date + ',' + selected_category + ',' + selected_amount[1:]
                break
        user_list[str(chat_id)]['data'] = data_edit
        helper.write_json(user_list)
        bot.reply_to(m, "Date is updated")
    else :
        text_intro = "Cancelled the operation.\nSelect "
        commands = helper.getExitCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            text_intro += "/" + c + " to "
            text_intro += commands[c] + "\n\n"
        bot.send_message(m.chat.id, text_intro)


def edit_cat(m, bot, selected_data):
    user_list = helper.read_json()
    chat_id = m.chat.id
    data_edit = helper.getUserHistory(chat_id)
    new_cat = "" if m.text is None else m.text
    if new_cat != 'Cancel' :
        for i in range(len(data_edit)):
            user_data = data_edit[i].split(',')
            selected_date = selected_data[0].split('=')[1]
            selected_category = selected_data[1].split('=')[1]
            selected_amount = selected_data[2].split('=')[1]
            if user_data[0] == selected_date and user_data[1] == selected_category and user_data[2] == selected_amount[1:]:
                data_edit[i] = selected_date + ',' + new_cat + ',' + selected_amount[1:]
                break

        user_list[str(chat_id)]['data'] = data_edit
        helper.write_json(user_list)
        bot.reply_to(m, "Category is updated")
    else :
        text_intro = "Cancelled the operation.\nSelect "
        commands = helper.getExitCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            text_intro += "/" + c + " to "
            text_intro += commands[c] + "\n\n"
        bot.send_message(m.chat.id, text_intro)


def edit_cost(m, bot, selected_data):
    user_list = helper.read_json()
    new_cost = "" if m.text is None else m.text
    if new_cost != 'Cancel':
        chat_id = m.chat.id
        data_edit = helper.getUserHistory(chat_id)

        if helper.validate_entered_amount(new_cost) != 0:
            for i in range(len(data_edit)):
                user_data = data_edit[i].split(',')
                selected_date = selected_data[0].split('=')[1]
                selected_category = selected_data[1].split('=')[1]
                selected_amount = selected_data[2].split('=')[1]
                if user_data[0] == selected_date and user_data[1] == selected_category and user_data[2] == selected_amount[1:]:
                    data_edit[i] = selected_date + ',' + selected_category + ',' + new_cost
                    break
            user_list[str(chat_id)]['data'] = data_edit
            helper.write_json(user_list)
            bot.reply_to(m, "Expense amount is updated")
        else:
            bot.reply_to(m, "The cost is invalid")
            return
    else:
        text_intro = "Cancelled the operation.\nSelect "
        commands = helper.getExitCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            text_intro += "/" + c + " to "
            text_intro += commands[c] + "\n\n"
        bot.send_message(m.chat.id, text_intro)

