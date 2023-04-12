import requests

def get_user_prompt():
    prompt = input("Please enter a prompt: ")
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