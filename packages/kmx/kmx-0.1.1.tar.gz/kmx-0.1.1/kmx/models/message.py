from pydantic import BaseModel


class Message(BaseModel):
    """ """
    code: str
    data: dict


class MessageEnvelope(BaseModel):
    """ """
    sender: str
    receiver: str
    message: Message
    reply_to: Message | None
