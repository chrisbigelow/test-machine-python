import requests
import os
import openai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the ChatGPT API key from the environment variable
chatgpt_api_key = os.environ.get("CHATGPT_API_KEY")

if chatgpt_api_key:
    print("API key loaded successfully.")
    openai.api_key = chatgpt_api_key
else:
    print("Failed to load API key. Make sure the .env file is properly configured.")



def get_language():




def get_user_prompt():
    prompt = input("Define your first test case: ")
    return prompt

def send_prompt_to_api(prompt):
    url = "https://your_api_endpoint"  # Replace with the actual API endpoint
    data = {"prompt": prompt}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Prompt successfully sent to the API!")
    else:
        print(f"Error: {response.status_code}. Failed to send prompt to the API.")

def main():
    while True:
        user_prompt = get_user_prompt()
        if user_prompt.lower() == "exit":
            break
        send_prompt_to_api(user_prompt)
        print("Enter 'exit' to quit the program or just enter another prompt.")

if __name__ == "__main__":
    main()