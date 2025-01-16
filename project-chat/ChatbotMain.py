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
    print("\033[0;34mWelcome to the Poppleton Interactive Chat!\033[0m")
    print("\033[0;31mAll the chat data are being recorded and saved for training purposes!\033[0m")

    User = Username()
    agent_name = Available_agents()
    print(f"\n\033[0;36mHello {User}! How can I assist you today?\033[0m")
    print(f"\033[0;36mYou're now chatting with {agent_name}.\033[0m\n")

    responses = read_response_file()
    conversation = []

    # Generate a random number for disconnect
    disconnect_count = random.randint(6, 8)
    interaction_count = 0

    chat_loop(User, agent_name, responses, conversation, interaction_count, disconnect_count)


def Username():
    user_name = input("\n\033[0;90mPlease enter your name: \033[0m")
    Corrected_username = user_name[0].upper() + user_name[1:].lower()
    return Corrected_username


def Available_agents():
    agents = ["Steve", "ElDiablo", "Human", "Dana", "Kiyotaka", "Steven", "Mario", "Luigi"]
    return random.choice(agents)


def read_response_file():
    try:
        with open("responses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("\033[1;31mError: responses.json file not found!.\033[0m")
        exit()


def record_conversation(user, agent, conversation):
    filename = f"{user}_conversation.txt"

    with open(filename, "a") as file:
        file.write(f"Conversation between {user} and Agent {agent} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n")

        for line in conversation:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{timestamp} - {line}\n")


def disconnect_agent(user, agent, conversation):
    print("\033[1;31mSorry for the interruption but it seems like you have Disconnected\033[0m")
    conversation.append("Disconnected!")
    record_conversation(user, agent, conversation)

    conversation.clear()

    reconnect = input("\033[1;32mWould you like to reconnect? (Y/N): \033[0m").strip().lower()
    if reconnect == "y":
        conversation.append("\nReconnected Successfully!\n")
        record_conversation(user, agent, conversation)
        reconnect_session(user, read_response_file())  
    else:
        print(f"\033[1;33m{agent}: Have a great day, {user}! Goodbye!\033[0m")



def chat_loop(user, agent_name, responses, conversation, interaction_count, disconnect_count):
    while True:
        user_message = input(f"\033[0;97m{user}: \033[0m").lower()
        conversation.append(f"{user}: {user_message}")
        interaction_count += 1

        if interaction_count == disconnect_count:
            disconnect_agent(user, agent_name, conversation)
            break

        if user_message in ["bye", "exit"]:
            print(f"\033[0;32m{agent_name}: It was nice chatting with you, {user}! Goodbye!\033[0m")
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

        # Replaces {name} with the actual user name in the response in the json file
        response = response.replace("{name}", user)

        print(f"\033[0;32m{agent_name}: {response}.\033[0m") 
        conversation.append(f"{agent_name}: {response}")


def Authentication():
    os.system('cls')
    admin_id = int(input("\033[1;32mAdmin ID: \033[0m"))
    admin_pass = input("\033[1;32mAdmin Password: \033[0m")
    if admin_id == 10037 and admin_pass == "Admin":
        print("\033[1;41mWelcome Admin! Please wait taking you to Admin Panel....\033[0m\n")
        Admin()
    else:
        print("\033[1;31mImposter!!!\033[0m")
        SelectionUI_Main()


def Admin():
    os.system('cls')
    print('''
       _____   _____   _____   _____         _______ _______  _____  __   _
      |_____] |     | |_____] |_____] |      |______    |    |     | | \  |
      |       |_____| |       |       |_____ |______    |    |_____| |  \_|
                                                                           
                     _______ ______  _______ _____ __   _                  
                     |_____| |     \ |  |  |   |   | \  |                  
                     |     | |_____/ |  |  | __|__ |  \_|                                    
    ''')
    print("\033[0;31mSuccessfully connected to the Admin Panel\033[0m\n")
    print("\033[0;31mWhat would you wish to configure?\033[0m")
    print("\033[0;33m1. Add Keywords and Responses \n2. Add Jokes \n3. Add Random Responses \n4. Exit\033[0m\n")
    while True:
        choice = int(input("\033[1;32mChoose your option: \033[0m"))
        if choice > 4 or choice <= 0:
            print("\033[1;31mPlease input valid option!!!\033[0m")
        else:
            break
    if choice == 1:
        Append_keywords()
    elif choice == 2:
        Append_jokes()
    elif choice == 3:
        Append_random_responses()
    elif choice == 4:
        print("\033[1;33mThank You for Configuration\033[0m")


def Append_keywords():
    responses = read_response_file()
    new_keyword = input("\033[1;32mEnter the new keyword: \033[0m").lower()
    new_reply = input("\033[1;32mEnter the reply for this keyword: \033[0m")

    if new_keyword in responses["keywords"]:
        print(f"\033[1;33mThe keyword '{new_keyword}' already exists with the following reply: '{responses['keywords'][new_keyword]}'\033[0m")
    else:
        responses["keywords"][new_keyword] = new_reply
        print(f"\033[1;32mKeyword '{new_keyword}' has been added successfully with reply: '{new_reply}'\033[0m")

        with open("responses.json", "w") as file:
            json.dump(responses, file, indent=4)


def Append_jokes():
    responses = read_response_file()
    new_jokes = input("\033[1;32mEnter the joke you like to add: \033[0m")
    responses["jokes"].append(new_jokes)
    print(f"\033[1;32mJoke added successfully: {new_jokes}\033[0m")

    with open("responses.json", "w") as file:
        json.dump(responses, file, indent=4)


def Append_random_responses():
    responses = read_response_file()
    new_random_responses = input("\033[1;32mEnter the random response you like to add: \033[0m")
    responses["random_responses"].append(new_random_responses)
    print(f"\033[1;32mRandom Response added successfully: {new_random_responses}\033[0m")

    with open("responses.json", "w") as file:
        json.dump(responses, file, indent=4)



def reconnect_session(user, responses):
    agent_name = Available_agents()  # Re-selecting a random agent
    print(f"\n\033[1;34mReconnecting... Welcome back, {user}!\033[0m")
    print(f"\033[1;34mYou're now chatting with {agent_name} again.\033[0m")

    # This calls the chat_loop function to handle the conversation
    chat_loop(user, agent_name, responses, [], 0, random.randint(6, 8))


SelectionUI_Main()
