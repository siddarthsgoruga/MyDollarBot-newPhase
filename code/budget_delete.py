import helper

# Define a function to delete the user's budget information
def run(message, bot):
    # Get the chat ID from the message
    chat_id = message.chat.id
    user_list = helper.read_json() # Read user data from the JSON file
    print(user_list)

    # Check if the chat ID exists in the user data
    if str(chat_id) in user_list:
        # Clear the user's overall and category budgets by setting them to None
        user_list[str(chat_id)]['budget']['overall'] = None
        user_list[str(chat_id)]['budget']['category'] = None
        
        # Update the user data with the modified budget information
        helper.write_json(user_list)
    
    # Send a message to the user to confirm that the budget has been deleted
    bot.send_message(chat_id, 'Budget deleted!')
