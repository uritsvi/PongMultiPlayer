import threading

from session import Session
import random
import string

class Sessions:
    def __init__(self):
        self.__sessions = {}
        self.__lock = threading.Lock()

    def create_random_session_id(self) -> str:
        while True:
            session_id = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
            if session_id not in self.__sessions:
                return session_id
    def remove_from_connect_session(self, session_id: str):
        if session_id in self.__sessions:
            del self.__sessions[session_id]

    def create(self, conn) -> str:
        with self.__lock:
            id = self.create_random_session_id()


            session = Session()
            self.__sessions[id] = session


            session.add_client(conn)
            return id

    def get_session(self, session_id: str):
        with self.__lock:
            return self.__sessions.get(session_id)

    def connect_to_existing(self, session_id: str, conn):
            session = self.get_session(session_id)
            if session is None:
                print("Session not found:", session_id)
                return None

            session.add_client(conn)
            return session


