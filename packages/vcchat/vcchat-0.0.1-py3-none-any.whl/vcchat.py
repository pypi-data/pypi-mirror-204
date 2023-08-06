import openai
import os

def start(api_key=None):
    if api_key:
        openai.api_key = api_key
    else:
        openai.api_key = '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'
    messages = [{"role": "system", "content": "You are a kind helpful assistant."}]
    while True:
        message = input("User: ")
        if message.strip() == "":
            file_path = input("Enter path of text file (leave blank for default 'a.txt' file): ")
            if file_path.strip() == "":
                file_path = os.path.join(os.path.dirname(__file__), "a.txt")
            try:
                with open(file_path, "r") as file:
                    text = file.read()
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                continue
            messages.append({"role": "user", "content": text})
        elif message == "bye":
            break
        elif len(message) > 2048:
            print("Message is too long. Please keep it under 2048 characters.")
            continue
        else:
            messages.append({"role": "user", "content": message})
            text = None
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except Exception as e:
            print("An error occurred:", str(e))
            break
        reply = chat.choices[0].message.content
        print(f"Bot: {reply}")
        messages.append({"role": "assistant", "content": reply})