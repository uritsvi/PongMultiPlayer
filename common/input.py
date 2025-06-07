KEY_UP_TYPE = "up"
KEY_DOWN_TYPE = "down"

class KeyDownEvent:
    def __init__(self, key: str):
        self.key: str = key

    def get_key(self):
        return self.key

    def get_type(self):
        return KEY_DOWN_TYPE

class KeyUpEvent:
    def __init__(self, key: str):
        self.key: str = key

    def get_key(self):
        return self.key

    def get_type(self):
        return KEY_UP_TYPE