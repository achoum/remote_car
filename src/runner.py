"""
Controls the car from joystick signals.
"""

import time
import math
import threading
import sys

from gpiozero import Device, LED, Motor, Servo, DigitalOutputDevice
import time
from gpiozero.pins.pigpio import PiGPIOFactory, PiGPIOPin


DIRECTION_MODE_DIRECT = 0
SPEED_MODE_DIRECT = 0
SPEED_MODE_SLOW_1 = 1


def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def evt(t, k, v):
    sys.stdout.write(f"{t} {k} {v}\n")


class Controller:

    def __init__(self):
        self.input_accelerator_ = 0
        self.input_direction_ = 0
        self.input_light = False
        self.last_input_light = False

        self.output_speed_ = 0
        self.output_direction_ = 0
        self.output_light = False

        self.output_debug_stream_ = False
        self.refresh_interval_ = 0.02
        self.connect_to_gpio_ = True

        self.power_engine_ = 1
        self.power_brake_ = 4
        self.mass_ = 10

        # Minimum and maximum value sent to the server when turning wheels.
        self.calibration_direction = (-0.8, 0.8)

        self.direction_mode = DIRECTION_MODE_DIRECT
        self.speed_mode = SPEED_MODE_DIRECT

        if self.connect_to_gpio_:
            Device.pin_factory = PiGPIOFactory()
            self.servo_forward_ = Motor(forward=6, backward=5, enable=11)
            self.servo_direction_ = Servo(13)
            self.light_ = DigitalOutputDevice(9)
            self.enable_light_ = DigitalOutputDevice(10)
        else:
            self.servo_forward_ = None
            self.servo_direction_ = None
            self.light_ = None
            self.enable_light_ = None

        self.thread_ = threading.Thread(
            target=self.thread_collect, daemon=True)
        self.thread_.start()

    def reset(self):
        if self.connect_to_gpio_:
            self.servo_direction_.value = None
            self.servo_forward_.forward(0)

    def thread_collect(self):
        for l in sys.stdin:
            try:
                s = l.strip().split(" ")
                evt_time = float(s[0])
                evt_key = s[1]
                evt_value = float(s[2])
                if evt_key == "accelerator":
                    self.input_accelerator_ = evt_value
                elif evt_key == "direction":
                    self.input_direction_ = evt_value
                elif evt_key == "light":
                    self.input_light = evt_value >= 0.5
                else:
                    print(f"Unknown event type {evt_key}", flush=True)
            except Exception as e:
                print(
                    f"Cannot parse line \"{l}\".\nException: {e}", flush=True)

    def output_evt(self, ttime):
        evt(ttime, "input_accelerator", self.input_accelerator_)
        evt(ttime, "input_direction", self.input_direction_)
        evt(ttime, "output_direction", self.output_direction_)
        evt(ttime, "output_speed", self.output_speed_)
        sys.stdout.flush()

    def unit_direction_to_servo_direction(self, v):
        if v >= 0:
            return v * self.calibration_direction[1]
        else:
            return -v * self.calibration_direction[0]

    def set_gpio(self):
        self.servo_direction_.value = self.unit_direction_to_servo_direction(
            -self.output_direction_)
        if self.output_speed_ >= 0:
            self.servo_forward_.forward(self.output_speed_)
        else:
            self.servo_forward_.backward(-self.output_speed_)

    def run(self):
        while True:
            ttime = time.time()

            if self.input_light != self.last_input_light:
                self.last_input_light = self.input_light

                if self.input_light:
                    # Switch light
                    self.output_light = not self.output_light
                    self.light_.value = self.output_light
                    self.enable_light_.value = self.output_light

            if self.direction_mode == DIRECTION_MODE_DIRECT:
                self.output_direction_ = self.input_direction_
            else:
                raise ValueError("Non supported direction mode")

            if self.speed_mode == SPEED_MODE_DIRECT:
                self.output_speed_ = self.input_accelerator_
            elif self.speed_mode == SPEED_MODE_SLOW_1:

                abs_speed = abs(self.output_speed_)

                # delta_dir: Signed direction of the speed change.
                if self.input_accelerator_ > self.output_speed_:
                    delta_dir = 1
                elif self.input_accelerator_ < self.output_speed_:
                    delta_dir = -1
                else:
                    delta_dir = 0

                # enevery_dir: Signed direction of the energy change.
                if self.output_speed_ * delta_dir >= 0:
                    power = self.power_engine_
                    enevery_dir = 1
                else:
                    power = self.power_brake_
                    enevery_dir = -1

                # car_dir: Direction of the car
                if self.output_speed_ > 0:
                    car_dir = 1
                elif self.output_speed_ < 0:
                    car_dir = -1
                else:
                    car_dir = delta_dir

                square_speed = abs_speed*abs_speed + 2 * enevery_dir * \
                    power * self.refresh_interval_ / self.mass_
                if square_speed > 1:
                    square_speed = 1
                if square_speed < 0:
                    square_speed = 0
                self.output_speed_ = math.sqrt(square_speed) * car_dir

            else:
                raise ValueError("Non supported speed mode")

            if self.output_debug_stream_:
                self.output_evt(ttime)

            if self.connect_to_gpio_:
                self.set_gpio()

            time.sleep(self.refresh_interval_)


def main():
    conroller = None
    try:
        errprint("Start controller")
        conroller = Controller()
        errprint("Run controller")
        conroller.run()
    except Exception as e:
        errprint("Interrupted:", e)
        if conroller is not None:
            conroller.reset()
        raise e

    errprint("Reset")
    if conroller is not None:
        conroller.reset()
    errprint("Done")


main()
