import time

from common.common import TARGET_FRAME_TIME


class Fps:
    def __init__(self):
        self.start_time = 0

    def start_frame(self):
        """Start the frame timer."""
        self.start_time = time.time()

    def end_frame(self):
        """End the frame timer and return the elapsed time."""
        elapsed_time = time.time() - self.start_time
        sleep_time = max(0, TARGET_FRAME_TIME - elapsed_time)
        time.sleep(sleep_time)