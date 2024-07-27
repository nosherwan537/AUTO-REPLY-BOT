import os
import time
import pyautogui
import pyperclip
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the configuration for the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    
)

# Extract WhatsApp chat history
def extract_chat_history():
    time.sleep(3)  # Pause to allow time to switch to the target window

    # Click on the WhatsApp window or chat (coordinates may vary)
    pyautogui.click(1268, 1065)
    time.sleep(0.5)  # Short pause to ensure the click is registered

    # Drag to select the chat text (coordinates may vary)
    pyautogui.moveTo(884, 282)
    pyautogui.dragTo(903, 988, duration=1)  # duration makes the drag smooth

    # Copy the selected text to the clipboard
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)  # Short pause to ensure the text is copied

    # Click to close the chat window (if necessary)
    pyautogui.click(1268, 1065)  # Click on the icon again to close the window

    # Get the clipboard content
    chat_history = pyperclip.paste()
    return chat_history

# Generate a response based on the chat history
def generate_response(chat_history):
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [{"text": chat_history}]}
        ]
    )
    response = chat_session.send_message("Reply to the message , act as me , friends often do casual chat on whatsapp, so dont respond I can't answer this or that , you have to act as me and have to answer no matter what , keep it precise , you can also send message in urdu if someone chats in urdu or in roman urdu, message as normal human , no need of Name and Date mentioned before message , it is Whatsapp , dont act as a bot, act as human , send relevant messages and dont keep on sending at once ")
    return response.text
# Send a message in WhatsApp
def send_message(message):
    time.sleep(3)  # Pause to allow time to switch to the WhatsApp input field
    pyautogui.click(1123, 968)  # Click on the input field (coordinates may vary)
    time.sleep(0.5)
    pyautogui.typewrite(message, interval=0.05)  # Type the message
    pyautogui.hotkey('enter')  # Send the message

# Main workflow
def main():
    chat_history = extract_chat_history()
    print("Chat History:", chat_history)

    response = generate_response(chat_history)
    print("Generated Response:", response)

    send_message(response)

if __name__ == "__main__":
    main()
