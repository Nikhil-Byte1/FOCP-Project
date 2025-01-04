import random
import json
import os

def SelectionUI():
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

    while True:
        user_message = input(f"{User}: ").lower()

        if user_message in ["bye", "quit", "exit"]:
            print(f"{agent_name}: It was nice chatting with you, {User}! Goodbye!")
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

        # Display response with colored text
        print(f"\033[0;32m{agent_name}: {response}.\033[0m")  # Green text


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
        print("Error: responses.json file not found! Ensure the file is in the same directory as the script.")
        exit()

def Authentication():
    os.system('cls')
    admin_id=int(input("Admin ID: "))
    admin_pass=input("Admin Password: ")
    if admin_id==10037 and admin_pass=="Admin":
        print("Welcome Admin! Please wait taking you to Admin Panel....")
        Admin()
    else:
        print("Imposter!!!")
        SelectionUI()
  
 
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
    print("Successfully connected to the Admin Panel")
    print("What would you wish to configure?")
    print("1. Add Keywords and Responses \n2. Add Jokes \n3. Add Random Responses \n4. Exit")
    while True:
       choice=int(input("Choose your option: "))
       if choice > 4 or choice <=0:
         print("Please input valid option!!!")
       else:
           break
    if choice == 1:
        Append_keywords()
    elif choice ==2:
        Append_jokes()  
    elif choice == 3:
        Append_random_responses() 
    elif choice == 4:
        print("Thank You for Conf") 
   




def Append_keywords():
    responses = load_responses()
    new_keyword = input("Enter the new keyword: ").lower() 
    new_reply = input("Enter the reply for this keyword: ")

    
    if new_keyword in responses["keywords"]:
        print(f"The keyword '{new_keyword}' already exists with the following reply: '{responses['keywords'][new_keyword]}'")
    else:
      
        responses["keywords"][new_keyword] = new_reply
        print(f"Keyword '{new_keyword}' has been added successfully with reply: '{new_reply}'")
        
        # Save the updated data back to the JSON file
        with open("responses.json", "w") as file:
            json.dump(responses, file, indent=4)


def Append_jokes():
    responses = load_responses()
    new_jokes= input("Enter the joke you like to add: ")
    
    responses["jokes"].append(new_jokes)
    print(f"Joke added successfully: {new_jokes}")

    with open("responses.json", "w") as file:
        json.dump(responses, file, indent=4)


def Append_random_responses():
    responses = load_responses()
    new_random_responses= input("Enter the random response you like to add: ")
    
    responses["random_responses"].append(new_random_responses)
    print(f"Random Response added successfully: {new_random_responses}")

    with open("responses.json", "w") as file:
        json.dump(responses, file, indent=4)

SelectionUI()
