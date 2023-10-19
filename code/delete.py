import helper

# Define a function to delete the expense history
def run(message, bot):
    global user_list
    chat_id = message.chat.id
    delete_history_text = ""
    user_list = helper.read_json()

    # Check if the user has any expense history
    if (str(chat_id) in user_list):
        # Call the deleteHistory function to remove the history
        helper.write_json(deleteHistory(chat_id))
        delete_history_text = "History has been deleted!"
    else:
        delete_history_text = "No records there to be deleted. Start adding your expenses to keep track of your spendings!"
    # Send a message to the user indicating the status of history deletion
    bot.send_message(chat_id, delete_history_text)


# Function to delete the expense history for a specific user
def deleteHistory(chat_id):
    global user_list
    if (str(chat_id) in user_list):
        del user_list[str(chat_id)]
    return user_list
