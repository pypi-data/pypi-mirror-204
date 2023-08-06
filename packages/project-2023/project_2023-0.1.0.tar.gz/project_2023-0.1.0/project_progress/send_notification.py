import os
import json
import email
from .slack_bot import sendSlackWebhook

current_dir = os.path.dirname(os.path.abspath(__file__))
emails_path = os.path.join(current_dir, "emails.json")


def find_encoding_info(txt):
    info = email.header.decode_header(txt)
    subject, encode = info[0]
    return subject, encode


# Read email data from the local JSON file
with open(emails_path, "r") as file:
    emails = json.load(file)

# Process the emails
for email_message in emails:
    email_from = email_message["From"]
    email_date = email_message["Date"]
    subject_str = email_message["Subject"]

    # Enter the keyword you want to filter out of the email.
    # If the program finds the keyword, it returns the location. Otherwise, it returns -1.
    # In this case, the program will find the email that contains "Thank you" in the content.
    # You can customize the word you want to find in your email.
    if subject_str.find("Thank you") >= 0:
        slack_send_message = email_from + "\n" + email_date + "\n" + subject_str
        webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "https://example.com/mock_url")
        sendSlackWebhook(slack_send_message, webhook_url)
        print(slack_send_message)
