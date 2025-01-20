from flask import Flask, request
import requests

app = Flask(__name__)

# Replace these with your values
PAGE_ACCESS_TOKEN = "your_page_access_token_here"
VERIFY_TOKEN = "your_verify_token_here"

# Facebook Messenger API URL
FB_API_URL = "https://graph.facebook.com/v16.0/me/messages"


# Verify webhook
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        return challenge
    return "Unauthorized", 403


# Handle incoming messages
@app.route('/webhook', methods=['POST'])
def handle_messages():
    data = request.get_json()
    if "object" in data and data["object"] == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                if "message" in event:
                    sender_id = event["sender"]["id"]
                    if "text" in event["message"]:
                        message_text = event["message"]["text"]
                        reply = generate_reply(message_text)
                        send_message(sender_id, reply)
    return "Event received", 200


# Generate an automatic reply
def generate_reply(message_text):
    message_text = message_text.lower()
    if "hello" in message_text or "hi" in message_text:
        return "Hello! How can I assist you today?"
    elif "help" in message_text:
        return "Sure, I'm here to help! Please tell me more about your issue."
    elif "bye" in message_text:
        return "Goodbye! Have a great day!"
    else:
        return "I'm an auto admin bot. Let me know if you need assistance."


# Send a message to the user
def send_message(recipient_id, message_text):
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(
        FB_API_URL,
        headers=headers,
        params={"access_token": PAGE_ACCESS_TOKEN},
        json=payload
    )
    if response.status_code != 200:
        print(f"Unable to send message: {response.text}")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
