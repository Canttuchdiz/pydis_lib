import json


class Message:

    """
    The message object which contains content, author, and channel
    """

    __slots__ = (

        'content',
        'mentions',
        'author',
        'reactions',
        'reference',
    )


    def __init__(self, event : str, payload):

        self.content = payload["d"]["content"]


