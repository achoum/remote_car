"""
Send joysticks signal remotely.
"""

import time
import xbox_controller
import sys

MAX_UPDATE_INTERVAL = 0.50
MIN_UPDATE_INTERVAL = 0.02


class Controller:

    def __init__(self):
        self.joy_ = xbox_controller.XboxController()
        self.begin_time_ = 0  # time.time()
        self.last_sync_ = {}
        self.has_sync_ = False

    def sync(self, cur_time, key, value):

        # Get the item
        if key not in self.last_sync_:
            item = [-1, -1]  # Last update, last value
            self.last_sync_[key] = item
        else:
            item = self.last_sync_[key]

        if value != item[1] or cur_time > item[0] + MAX_UPDATE_INTERVAL:
            item[1] = value
            item[0] = cur_time
            self.has_sync_ = True
            sys.stdout.write(f"{cur_time} {key} {value}\n")

    def end_frame(self):
        if self.has_sync_:
            self.has_sync_ = False
            sys.stdout.flush()

    def run(self):
        while True:
            if self.joy_.exception is not None:
                raise self.joy_.exception

            cur_time = time.time() - self.begin_time_

            self.sync(cur_time, "accelerator",
                      self.joy_.RightTrigger - self.joy_.LeftTrigger)

            self.sync(cur_time, "direction",
                      self.joy_.LeftJoystickX)

            self.sync(cur_time, "light",                      self.joy_.A)

            self.end_frame()
            time.sleep(MIN_UPDATE_INTERVAL)


def main():

    conroller = Controller()
    conroller.run()


main()
