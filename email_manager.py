import json
import os
import random
import string

from simplegmail import Gmail


def generate_random_name(length=8):
    characters = string.ascii_letters
    return ''.join(random.choice(characters) for _ in range(length))


class EmailManager:
    def __init__(self, gmail_payload):
        self.gmail_payload = gmail_payload
        self.file = f"{generate_random_name()}.json"
        with open(self.file, 'w') as f:
            json.dump(self.gmail_payload, f)
        self.gmail = Gmail(
            creds_file=self.file
        )
        self.gmail.maxResults = 4

    def fetch_inbox(self):
        messages = self.gmail.get_messages()
        return messages

    def fetch_sent(self):
        messages = self.gmail.get_sent_messages()
        return messages

    def fetch_starred(self):
        messages = self.gmail.get_starred_messages()
        return messages

    def send_email(self, sender, to_email, subject, body):
        params = {
            "sender": sender,
            "to": to_email,
            "subject": subject,
            "msg_plain": body,
        }
        self.gmail.send_message(**params)

    def stop(self):
        os.remove(self.file)
