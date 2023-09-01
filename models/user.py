from dataclasses import dataclass

from pydantic import BaseModel
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    gmail_payload = fields.JSONField()


class GetEmailReq(BaseModel):
    email: str
    req_type: int


class SendEmailReq(BaseModel):
    email: str
    to_email: str
    subject: str
    body: str


class AuthReq(BaseModel):
    email: str
    gmail_payload: dict


@dataclass
class Message:
    name: str
    datetime: str
    subject: str
    body: str
    email: str
    id: str
    image: str

    def to_json(self):
        return {
            "name": self.name,
            "datetime": self.datetime,
            "subject": self.subject,
            "body": self.body,
            "email": self.email,
            "id": self.id,
            "image": self.image
        }
