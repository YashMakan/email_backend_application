import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from email_manager import EmailManager
from models.user import GetEmailReq, User, Message, SendEmailReq, AuthReq

app = FastAPI()

register_tortoise(
    app,
    db_url=f"sqlite://db.sqlite",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.post('/get-emails')
async def get_emails(req: GetEmailReq):
    user = await User.filter(email=req.email).get()
    messages = []
    try:
        manager = EmailManager(user.gmail_payload)
        if req.req_type == 0:
            messages = manager.fetch_inbox()
        elif req.req_type == 1:
            messages = manager.fetch_sent()
        elif req.req_type == 2:
            messages = manager.fetch_starred()
        else:
            return {'status': False, 'message': 'Invalid req_type is passed!'}
        manager.stop()
    except Exception as e:
        print(e)
    messages = list(map(lambda msg: Message(
        email=msg.recipient,
        id=msg.id,
        subject=msg.subject,
        datetime=msg.date,
        body=msg.plain,
        name=msg.headers['From'],
        image=""  # msg.headers['From'],
    ).to_json(), messages))
    return {'status': True, "data": messages}


@app.put('/send-email')
async def test_endpoint(req: SendEmailReq):
    user = await User.filter(email=req.email).get()
    manager = EmailManager(user.gmail_payload)
    manager.send_email(
        sender=req.email,
        to_email=req.to_email,
        subject=req.subject,
        body=req.body,
    )
    return {'status': True, 'message': 'Email is successfully sent!'}


@app.post('/authenticate')
async def test_endpoint(req: AuthReq):
    user = await User.get_or_none(email=req.email)
    if user:
        await User.filter(email=req.email).delete()
    await User.create(email=req.email, gmail_payload=req.gmail_payload)
    return {'status': True, 'message': 'User authenticated successfully'}


if __name__ == "__main__":
    uvicorn.run(app)
