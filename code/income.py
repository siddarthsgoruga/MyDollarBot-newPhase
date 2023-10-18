import helper
import budget_view
import budget_update
import budget_delete
import logging
from telebot import types


def run(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    options = helper.getOptions()
    markup.row_width = 2
    for c in options.values():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Operation or Select Cancel to cancel the operation', reply_markup=markup)
    bot.register_next_step_handler(msg, post_operation_selection, bot)


def post_operation_selection(message, bot):
    try:
        chat_id = message.chat.id
        op = message.text
        options = helper.getOptions()

        if op not in options.values():
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this operation \"{}\"!".format(op))
        
        if op == options['update']:
            chat_id = message.chat.id
            if (helper.isTotalIncomeAvailable(chat_id)):
                chat_id = message.chat.id
                currentIncome = helper.getTotalIncome(chat_id)
                msg_string = 'Current income is ${}\n\nEnter your new monthly income(Enter numeric values only) or enter Cancel to cancel the operation'
                message = bot.send_message(chat_id, msg_string.format(currentIncome))
            else:
                message = bot.send_message(chat_id, 'Enter your monthly income(Enter numeric values only) or enter Cancel to cancel the operation')
            bot.register_next_step_handler(message, post_overall_amount_input, bot)

        elif op == options['view']:
            chat_id = message.chat.id
            if (helper.isTotalIncomeAvailable(chat_id)):
                display_income(message, bot)
            else:
                raise Exception('Income does not exist. Use ' + helper.getOptions()['update'] + ' option to add/update the income')

        elif op == options['delete']:
            delete_income(message, bot)
        elif op == 'Cancel':
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(chat_id, text_intro)
        else:
          bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
          raise Exception("Sorry I don't recognise this operation \"{}\"!".format(op))

    except Exception as e:
        # print("hit exception")
        helper.throw_exception(e, message, bot, logging)


def post_overall_amount_input(message, bot):
    try:
        chat_id = message.chat.id
        if message.text != 'Cancel' :
            amount_value = helper.validate_entered_amount(message.text)

            if amount_value == 0:
                raise Exception("Invalid amount.")
            user_list = helper.read_json()
            if str(chat_id) not in user_list:
                user_list[str(chat_id)] = helper.createNewUserRecord()
            
            user_list[str(chat_id)]['income'] = amount_value
            helper.write_json(user_list)
            bot.send_message(chat_id, 'Income Updated!')
            return user_list
        else :
            text_intro = "Cancelled the operation.\nSelect "
            commands = helper.getExitCommands()
            for c in commands:  # generate help text out of the commands dictionary defined at the top
                text_intro += "/" + c + " to "
                text_intro += commands[c] + "\n\n"
            bot.send_message(chat_id, text_intro)
    except Exception as e:
        helper.throw_exception(e, message, bot, logging)   


def display_income(message, bot):
    chat_id = message.chat.id
    data = helper.getTotalIncome(chat_id)
    bot.send_message(chat_id, 'Total Income: $' + data)


def delete_income(message, bot):
    chat_id = message.chat.id
    user_list = helper.read_json()
    print(user_list)
    if str(chat_id) in user_list:
        user_list[str(chat_id)]['income'] = None
        helper.write_json(user_list)
    bot.send_message(chat_id, 'Income deleted!')

