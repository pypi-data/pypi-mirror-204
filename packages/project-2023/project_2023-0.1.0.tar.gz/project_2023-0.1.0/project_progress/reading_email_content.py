import email
from email import policy


def find_encoding_info(txt):
    info = email.header.decode_header(txt)
    subject, encode = info[0]
    return subject, encode


def read_email_contents(imap, num_emails=5):
    email_contents = []

    imap.select("INBOX")
    resp, data = imap.uid("search", None, "All")
    all_email = data[0].split()
    last_email = all_email[-num_emails:]

    for mail in reversed(last_email):
        result, data = imap.uid("fetch", mail, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email, policy=policy.default)

        subject, encode = find_encoding_info(email_message["Subject"])

        message = ""
        if email_message.is_multipart():
            for part in email_message.get_payload():
                if part.get_content_type() == "text/plain":
                    bytes = part.get_payload(decode=True)
                    encode = part.get_content_charset()
                    message = message + str(bytes, encode)

        email_contents.append(
            (
                email_message["From"],
                email_message["Sender"],
                email_message["To"],
                email_message["Date"],
                subject,
                message,
            )
        )

    return email_contents
