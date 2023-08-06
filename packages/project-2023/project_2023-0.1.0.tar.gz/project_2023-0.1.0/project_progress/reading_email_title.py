import email
from email import policy


def find_encoding_info(txt):
    info = email.header.decode_header(txt)
    subject, encode = info[0]
    return subject, encode


def read_email_titles(imap, num_emails=5):
    email_titles = []

    imap.select("INBOX")
    resp, data = imap.uid("search", None, "All")
    all_email = data[0].split()
    last_email = all_email[-num_emails:]

    for mail in reversed(last_email):
        result, data = imap.uid("fetch", mail, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email, policy=policy.default)

        subject, encode = find_encoding_info(email_message["Subject"])
        email_titles.append(
            (email_message["From"], email_message["Sender"], email_message["To"], email_message["Date"], subject)
        )

    return email_titles
