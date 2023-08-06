import requests


def sendSlackWebhook(message, webhook_url):
    if webhook_url == "https://example.com/mock_url":
        print("Mock webhook: " + message)
    else:
        payload = {"text": message}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
