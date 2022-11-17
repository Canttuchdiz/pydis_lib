
class Message:

    __slots__ = (

        'content',
        'mentions',
        'author',
        'reactions',
        'reference',
    )


    def __init__(self, payload, content : str):
        self._payload = payload
        self.content : str = payload['content']
