import time
import math
import threading
import sys

from gpiozero import Device, LED, Motor, Servo
import time
from gpiozero.pins.pigpio import PiGPIOPin
from gpiozero.pins.pigpio import PiGPIOFactory

from gpiozero import LED
from gpiozero import Buzzer
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone


def led():
    led = LED(21)
    led.blink(on_time=1, off_time=1, n=5, background=False)


def buzzer():
    bz = Buzzer(12)
    bz.beep(on_time=1, off_time=1, n=5, background=False)
    bz.stop()


def tonebuzzer():
    bz = TonalBuzzer(12)
    notes = [262, 294, 330, 262, 262, 294, 330, 262, 330, 349, 392, 330, 349, 392, 392,
             440, 392, 349, 330, 262, 392, 440, 392, 349, 330, 262, 262, 196, 262, 262, 196, 262]
    durations = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.25,
                 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 1]
    for note, duration in zip(notes, durations):
        bz.play(Tone.from_frequency(note))
        time.sleep(duration)
    bz.stop()


def tonebuzzer2():
    bz = TonalBuzzer(12)
    bz.play(Tone(220.0))
    time.sleep(1)
    bz.stop()


def main():

    # led()
    # buzzer()
    # tonebuzzer()
    tonebuzzer2()

    print("done")


main()
