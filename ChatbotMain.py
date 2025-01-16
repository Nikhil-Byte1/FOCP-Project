import random
import json
import os
from datetime import datetime

def SelectionUI_Main():
    os.system('cls')
    print('''

    ___                  _      _                  ___ _           _   _           _   
   / _ \___  _ __  _ __ | | ___| |_ ___  _ __     / __\ |__   __ _| |_| |__   ___ | |_ 
  / /_)/ _ \| '_ \| '_ \| |/ _ \ __/ _ \| '_ \   / /  | '_ \ / _` | __| '_ \ / _ \| __| 
 / ___/ (_) | |_) | |_) | |  __/ || (_) | | | | / /___| | | | (_| | |_| |_) | (_) | |_ 
 \/    \___/| .__/| .__/|_|\___|\__\___/|_| |_| \____/|_| |_|\__,_|\__|_.__/ \___/ \__| 
            |_|   |_|                                                                  
                                                                                                                   
   \n''')
    print("Welcome to the Poppleton Interactive Chat!")
    print("\033[0;31mAll the chat data are being recorded and saved for training purposes!\033[0m")

    User = Username()
    agent_name = Available_agents()
    print(f"Hello {User}! How can I assist you today?")
    print(f"You're now chatting with {agent_name}.")

    responses = load_responses()
    conversation = []

    # Generate a random number for disconnect
    disconnect_count = random.randint(6, 8)
    interaction_count = 0

    chat_loop(User, agent_name, responses, conversation, interaction_count, disconnect_count)


def Username():
    user_name = input("Please enter your name: ")
    Corrected_username = user_name[0].upper() + user_name[1:].lower()
    return Corrected_username


def Available_agents():
    agents = ["Steve", "ElDiablo", "Charlie", "Dana", "Elliot"]
    return random.choice(agents)


def load_responses():
    try:
        with open("responses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: responses.json file not found!.")
        exit()

def record_conversation(user, agent, conversation):
    filename = f"{user}_conversation.txt"

    with open(filename, "a") as file:
        # Add the header only when the conversation is being written for the first time
        file.write(f"Conversation between {user} and Agent {agent} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n\n")

        # Append each line of the conversation with a timestamp
        for line in conversation:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{timestamp} - {line}\n")



def disconnect_agent(user, agent, conversation):
    print("Sorry for the interruption but it seems like you have Disconnected")
    conversation.append("Disconnected!")
    record_conversation(user, agent, conversation)

    # Clear conversation after recording to avoid repeating
    conversation.clear()

    reconnect = input("Would you like to reconnect? (Y/N): ").strip().lower()
    if reconnect == "y":
        conversation.append("Reconnected Successfully!\n")
        record_conversation(user, agent, conversation)
        reconnect_session(user, load_responses())  
    else:
        print(f"{agent}: Have a great day, {user}! Goodbye!")


def Authentication():
    os.system('cls')
    admin_id = int(input("Admin ID: "))
    admin_pass = input("Admin Password: ")
    if admin_id == 10037 and admin_pass == "Admin":
        print("Welcome Admin! Please wait taking you to Admin Panel....")
        Admin()
    else:
        print("Imposter!!!")
        SelectionUI_Main()


def Admin():
    os.system('cls')
    print('''

       _____   _____   _____   _____         _______ _______  _____  __   _
      |_____] |     | |_____] |_____] |      |______    |    |     | | \  |
      |       |_____| |       |       |_____ |______    |    |_____| |  \_|
                                                                           
                     _______ ______  _______ _____ __   _                  

    ''')
    print("Successfully connected to the Admin Panel")
    print("What would you wish to configure?")
    print("1. Add Keywords and Responses \n2. Add Jokes \n3. Add Random Responses \n4. Exit")
    while True:
        choice = int(input("Choose your option: "))
        if choice > 4 or choice <= 0:
            print("Please input valid option!!!")
        else:
            break
    if choice == 1:
        Append_keywords()
    elif choice == 2:
        Append_jokes()
    elif choice == 3:
        Append_random_responses()
    elif choice == 4:
        print("Thank You for Configuration")


def Append_keywords():
    responses = load_responses()
    new_keyword = input("Enter the new keyword: ").lower()
    new_reply = input("Enter the reply for this keyword: ")

    if new_keyword in responses["keywords"]:
        print(f"The keyword '{new_keyword}' already exists with the following reply: '{responses['keywords'][new_keyword]}'")
    else:
        responses["keywords"][new_keyword] = new_reply
        print(f"Keyword '{new_keyword}' has been added successfully with reply: '{new_reply}'")

        with open("responses.json", "w") as file:
            json.dump(responses, file, indent=4)


def Append_jokes():
    responses = load_responses()
    new_jokes = input("Enter the joke you like to add: ")
    responses["jokes"].append(new_jokes)
    print(f"Joke added successfully: {new_jokes}")

    with open("responses.json", "w") as file:
        json.dump(responses, file, indent=4)


def Append_random_responses():
    responses = load_responses()
    new_random_responses = input("Enter the random response you like to add: ")
    responses["random_responses"].append(new_random_responses)
    print(f"Random Response added successfully: {new_random_responses}")

    with open("responses.json", "w") as file:
        json.dump(responses, file, indent=4)


def chat_loop(user, agent_name, responses, conversation, interaction_count, disconnect_count):
    while True:
        user_message = input(f"{user}: ").lower()
        conversation.append(f"{user}: {user_message}")
        interaction_count += 1

        if interaction_count == disconnect_count:
            # Disconnect agent after certain messages
            disconnect_agent(user, agent_name, conversation)
            break

        if user_message in ["bye", "quit", "exit"]:
            print(f"{agent_name}: It was nice chatting with you, {user}! Goodbye!")
            conversation.append(f"{agent_name}: It was nice chatting with you, {user}! Goodbye!")
            record_conversation(user, agent_name, conversation)
            break

        if "admin access" in user_message:
            Authentication()
            break

        if "joke" in user_message:
            response = random.choice(responses["jokes"])
        else:
            matched_responses = [
                reply for keyword, reply in responses["keywords"].items() if keyword in user_message
            ]
            if matched_responses:
                response = " and ".join(matched_responses)
            else:
                response = random.choice(responses["random_responses"])

        # Replace {name} with the actual user name in the response
        response = response.replace("{name}", user)

        print(f"\033[0;32m{agent_name}: {response}.\033[0m")  # Green text
        conversation.append(f"{agent_name}: {response}")

def reconnect_session(user, responses):
    agent_name = Available_agents()  # Re-select a random agent
    print(f"\nReconnecting... Welcome back, {user}!")
    print(f"You're now chatting with {agent_name} again.")

    # Call the chat_loop function to handle the conversation
    chat_loop(user, agent_name, responses, [], 0, random.randint(6, 8))


SelectionUI_Main()
