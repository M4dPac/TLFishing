from threading import Thread
import time
import pynput
from pynput.keyboard import Key, Listener
from pynput.mouse import Button
from loguru import logger
from random import uniform

keyboard = pynput.keyboard.Controller()
mouse = pynput.mouse.Controller()


class Flag:
    def __init__(self) -> None:
        self._START = False

    @property
    def START(self):
        return self._START

    @START.setter
    def START(self, value):
        self._START = value


FLAG = Flag()


def tap_key(key: str, delay_p=1.0, delay_r=0.2):
    if len(key) > 1:
        key = getattr(Key, key)

    keyboard.press(key)
    time.sleep(uniform(delay_p, delay_p + 0.5))
    keyboard.release(key)
    time.sleep(uniform(delay_r, delay_r + 0.2))


def on_press(key):
    if key == Key.f12:
        text = ("Stop listener", "Start listener")[FLAG.START]
        logger.info(text + f" {FLAG.START}")
        FLAG.START = not FLAG.START


def mouse_movement(x, y):
    logger.debug(f"Move mouse to {x = }, {y = }")
    mouse.position = (x, y)


def mouse_click(button="l", count=1):
    if button not in "lr":
        raise ValueError

    logger.debug(f"Mouse click {button = }, {count = }")
    button = (Button.right, Button.left)[button == "l"]
    mouse.click(button, count)
    time.sleep(uniform(0.5, 1.0))


# Collect events until released
def start_listener():
    with Listener(on_press=on_press, daemon=True) as listener:
        listener.join()
