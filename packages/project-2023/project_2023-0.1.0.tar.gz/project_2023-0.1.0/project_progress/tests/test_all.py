import os
import imaplib
import json
from unittest.mock import patch
from project_progress.email_sending import send_email
from project_progress.file_attachment import send_email_with_attachment
from project_progress.reading_email_title import read_email_titles
from project_progress.reading_email_content import read_email_contents
from project_progress.slack_bot import sendSlackWebhook


current_dir = os.path.dirname(os.path.abspath(__file__))
emails_path = os.path.join(current_dir, "..", "emails.json")

with open(emails_path, "r") as file:
    sample_emails = json.load(file)


@patch("smtplib.SMTP")
def test_send_email(mock_smtp):
    for email_info in sample_emails:
        send_email(email_info)


@patch("smtplib.SMTP")
@patch("imaplib.IMAP4_SSL")
def test_send_email_with_attachment(mock_imap, mock_smtp):
    for email_info in sample_emails:
        send_email_with_attachment(
            "sender@example.com",
            "your_password",
            "smtp.example.com",
            587,
            email_info["To"],
            email_info["Subject"],
            email_info["text"],
            "project_progress/sample_file.txt",
        )


sample_imap_config = {
    "imap_name": "imap.example.com",
    "imap_port": 993,
    "email": "your_email@example.com",
    "password": "your_password",
}


def create_imap_object(imap_config):
    imap = imaplib.IMAP4_SSL(imap_config["imap_name"], imap_config["imap_port"])
    imap.login(imap_config["email"], imap_config["password"])
    return imap


@patch("imaplib.IMAP4_SSL")
def test_read_email_titles(mock_imap):
    imap = create_imap_object(sample_imap_config)
    sample_raw_email = b"Subject: Test email\r\n\r\nThis is a test email."
    mock_imap.return_value.uid.return_value = ('OK', [b"1 (BODY[] " + sample_raw_email + b")"])
    read_email_titles(imap)


@patch("imaplib.IMAP4_SSL")
def test_read_email_contents(mock_imap):
    imap = create_imap_object(sample_imap_config)
    sample_raw_email = b"Subject: Test email\r\n\r\nThis is a test email."
    mock_imap.return_value.uid.return_value = ('OK', [b"1 (BODY[] " + sample_raw_email + b")"])
    read_email_contents(imap)


@patch("requests.post")
def test_sendSlackWebhook(mock_post):
    webhook_url = "https://hooks.slack.com/services/your/webhook/url"
    sendSlackWebhook(webhook_url, "Test message")


@patch("smtplib.SMTP")
@patch("imaplib.IMAP4_SSL")
def test_email_integration(mock_smtp, mock_imap):
    # Send an email
    sample_email = sample_emails[0]
    send_email(sample_email)

    # Create IMAP object
    imap = create_imap_object(sample_imap_config)

    # Read email titles and check if the sent email's title is in the list
    titles = read_email_titles(imap)
    assert any(sample_email["Subject"] in title for title in titles)

    # Read email contents and check if the sent email's content is in the list
    contents = read_email_contents(imap)
    assert any(sample_email["text"] in content for content in contents)
