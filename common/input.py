class KeyDownEvent:
    def __init__(self, key: str):
        self.key: str = key

    def get_key(self):
        return self.key