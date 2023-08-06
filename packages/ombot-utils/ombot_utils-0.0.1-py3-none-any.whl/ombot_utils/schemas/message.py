from typing import List, Any
from pydantic import BaseModel
from .opt import Role, MessageType, SrcType, ChatStatus
from ..error_handler.error import VQLError


class DetObject(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        '''
        - bbox (List[float]): Bounding box of an object.
        - label (str): Object label.
        - conf (float): Object confidence.
        - attr (List[str]): Object attributes.
        '''
        super().__init__(**data)

    bbox: List[float]
    label: str
    conf: float
    attr: List[str] = []


class Message(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        '''
        - role (str): The role of this message. Choose from 'user', 'assistant', 'system'.
        - message_type (str): Type of the message. Choose from 'text' and 'image'.
        - src_type (str): Type of the message content. If message is text, src_type='text'. If message is image, Choose from 'url', 'base64', 'local' and 'redis'.
        - content (str): Message content.
        - objects (List[schemas.DetObject]): The detected objects.
        '''
        super().__init__(**data)

    role: Role
    message_type: MessageType
    src_type: SrcType
    content: str = ''
    objects: List[DetObject] = []


class ChatRecords(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        '''
        - bot_id (str): Unique id of a bot
        - session_id (str): Unique id of a chat session
        - dialog_id (str): Unique id of one single dialog
        - callback (str): Callback url.
        - message (schemas.Message): Message body.
        '''
        super().__init__(**data)

    bot_id: str
    session_id: str
    callback: str
    messages: List[Message]

    def get_recent(
        self, num: int = 1, role_include: list = [], role_exclude: list = []
    ) -> list:
        """
        Get most recent messages.
        :param num: Return message number, default 1. If num larger than legal message, return all legal ones.
        :param role_include: Only return message from include roles.
        :param role_exclude: Not return message from exclude roles.
        """
        if role_include and role_exclude:
            raise VQLError(
                999, msg='', detail='Do not use role_include and exclude at same time.'
            )

        output = []
        for message in reversed(self.messages):
            if (
                (role_include and message.role in role_include)
                or (role_exclude and message.role not in role_exclude)
                or (not role_include and not role_exclude)
            ):
                output.insert(0, message)
            if len(output) == num:
                break
        return output


class Reply(BaseModel):
    def __init__(__pydantic_self__, **data: Any) -> None:
        '''
        - code (int): Status code, 200 for success
        - error_info (str): Error information, empty string for success
        - took (int): Execution time (ms)
        - bot_id (str): Unique id of a bot
        - session_id (str): Unique id of a chat session
        - dialog_id (str): Unique id of one single dialog
        - status (str): Result status. 'incomplete' for incomplete dialog, 'end_block' for end of dialog, 'end_answer' for end of answer.
        - message (schemas.Message): Message body.
        '''
        super().__init__(**data)

    code: int
    error_info: str = ''
    took: int
    bot_id: str
    session_id: str
    dialog_id: str
    status: ChatStatus
    message: Message
