from threading import Thread
import mss
import pyautogui
import cv2 as cv
import numpy as np
import time
import multiprocessing
from loguru import logger
from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()

GLOBAL_START_FISHING = False
KEY_FLAG = True
FISHING_FLAG = False
START_FISHING_FLAG = False
FISHING_COUNT = 0
COUNT = 0
DELAY = 300


class bcolors:
    PINK = "\033[95m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    ENDC = "\033[0m"


class ScreenCaptureAgent:
    def __init__(self) -> None:
        self.text_color = (255, 255, 0)
        self.line_color = (0, 0, 255)

        self.img = None
        self.img_fishing = None

        self.capture_process = None
        self.fishing_thread = None
        self.fps = None
        self.enable_cv_preview = True
        self._start_fishing = False

        self.w, self.h = pyautogui.size()
        print("Разрешение экрана:" + " w: " + str(self.w) + " h: " + str(self.h))

        self.monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080, "mon": 2}

    @property
    def start_fishing(self):
        logger.info(f"Return start_fishing = {self._start_fishing}")
        time.sleep(1)
        return self._start_fishing

    @start_fishing.setter
    def start_fishing(self, value):
        logger.info("Set start_fishing")
        time.sleep(1)
        self._start_fishing = value

    def capture_screen(self) -> None:
        global KEY_FLAG, FISHING_FLAG, COUNT, DELAY, FISHING_COUNT
        Thread(target=start_listener, daemon=True).start()
        fps_report_time = time.time()
        fps_report_delay = 5
        n_frames = 1
        tmp_fishing_res = 0
        is_fish = ""
        fishing_res = 0

        with mss.mss() as sct:
            while True:

                self.img = sct.grab(self.monitor)
                self.img = np.array(self.img)

                self.img_fishing = self.img[594:709, 1101:1132]
                # img_fishing_grey = cv.cvtColor(self.img_fishing, cv.COLOR_BGR2GRAY)

                # result = self.img_fishing
                # template = cv.imread(
                #     r"D:\projects\TLFishing\images\start_fishing.png", 0
                # )
                # w, h = template.shape
                #
                # res = cv.matchTemplate(img_fishing_grey, template, cv.TM_CCOEFF_NORMED)
                # threshold = 0.8
                # loc = np.where(res >= threshold)
                # for pt in zip(*loc[::-1]):
                #     result = cv.rectangle(
                #         result, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2
                #     )

                img_hsv = cv.cvtColor(self.img_fishing, cv.COLOR_BGR2HSV)

                h = img_hsv.item(2, 9, 0)
                cv.rectangle(self.img_fishing, (6, 0), (11, 4), self.line_color, 1)
                cv.rectangle(self.img_fishing, (7, 0), (9, 111), self.line_color, 1)

                if GLOBAL_START_FISHING:
                    if not FISHING_FLAG and COUNT == 200:
                        logger.info("Press f")
                        tap_key("f", 0.5)
                        FISHING_COUNT += 1

                    if h <= 50:  # start fishing
                        if not FISHING_FLAG:
                            logger.info("Start fishing")
                        FISHING_FLAG = True
                        fish_bar = img_hsv[1:110, 8, 0]

                        if COUNT % 30 == 0:
                            fishing_res = (fish_bar >= 23).sum()

                            if fishing_res > tmp_fishing_res + 3:
                                tmp_fishing_res = fishing_res
                            else:
                                KEY_FLAG = not KEY_FLAG

                        if self.fishing_thread is None:
                            self.fishing_thread = Thread(
                                target=fishing_keyboard, daemon=True
                            )
                            self.fishing_thread.start()

                        is_fish = "Fish found"
                    else:  # end fishing
                        if self.fishing_thread is not None:
                            if FISHING_FLAG:
                                logger.info("End fishing")

                            self.fishing_thread = None
                            COUNT = 0
                            FISHING_FLAG = False

                        is_fish = "No fish found"

                    COUNT += 1
                else:
                    COUNT = 0
                    FISHING_FLAG = False
                    FISHING_COUNT = 0

                if self.enable_cv_preview:
                    small = cv.resize(self.img, (0, 0), fx=0.5, fy=0.5)
                    # big_fishing = cv.resize(self.img_fishing, (0, 0), fx=5, fy=5)

                    if self.fps is None:
                        fps_text = ""
                    else:
                        fps_text = f"FPS: {self.fps:.2f}"

                    for i, text in enumerate(
                        (
                            fps_text,
                            is_fish,
                            f"{fishing_res = }",
                        ),
                        1,
                    ):
                        cv.putText(
                            small,
                            text,
                            (25, 50 * i),
                            cv.FONT_HERSHEY_COMPLEX_SMALL,
                            1,
                            self.text_color,
                            1,
                            cv.LINE_AA,
                        )

                    # cv.imshow("Computer Vision", small)
                    cv.imshow("Total screen", small)
                    # cv.imshow("Fishing Bar", big_fishing)
                    cv.waitKey(1)

                    elapsed_time = time.time() - fps_report_time
                    if elapsed_time >= fps_report_delay:
                        self.fps = n_frames / elapsed_time
                        # print("FPS: " + str(self.fps))
                        n_frames = 0
                        fps_report_time = time.time()
                    n_frames += 1

    def is_process(self):
        return self.capture_process is not None

    def terminate_process(self) -> None:
        self.capture_process.terminate()
        self.capture_process = None


def print_menu():
    print(f"\n{bcolors.PINK}Command Menu{bcolors.ENDC}")
    print(f"\t{bcolors.GREEN}r - run\tStart screen capture{bcolors.ENDC}")
    print(f"\t{bcolors.RED}s - stop\tStop screen capture{bcolors.ENDC}")
    print(f"\tq - quit\tQuit the program")


def fishing_keyboard():
    while FISHING_FLAG and GLOBAL_START_FISHING:
        if COUNT % DELAY == 0:
            logger.info("Fishing")
        if KEY_FLAG:
            tap_key("a")
        else:
            tap_key("d")


def tap_key(key: str, delay_p=1.0, delay_r=0.4):
    keyboard.press(key)
    time.sleep(delay_p)
    keyboard.release(key)
    time.sleep(delay_r)


def on_press(key):
    global GLOBAL_START_FISHING

    if key == Key.f12:
        text = ("Start Fishing", "End Fishing")[GLOBAL_START_FISHING]
        GLOBAL_START_FISHING = not GLOBAL_START_FISHING
        logger.info(text + f" {GLOBAL_START_FISHING}")


# Collect events until released
def start_listener():
    with Listener(on_press=on_press, daemon=True) as listener:
        listener.join()


if __name__ == "__main__":

    screen_agent = ScreenCaptureAgent()

    while True:
        print_menu()
        user_input = input().lower()[0]

        match user_input:
            case "q":  # quit
                if screen_agent.is_process():
                    screen_agent.terminate_process()
                break
            case "r":  # run
                if screen_agent.is_process():
                    print(
                        f"{bcolors.YELLOW}WARNING:{bcolors.ENDC} Capture prcess already running."
                    )
                    continue

                screen_agent.capture_process = multiprocessing.Process(
                    target=screen_agent.capture_screen,
                    args=(),
                    name="screen capturre process",
                    daemon=True,
                )
                screen_agent.capture_process.start()
            case "s":  # stop
                if not screen_agent.is_process():
                    print(
                        f"{bcolors.YELLOW}WARNING:{bcolors.ENDC} Capture prcess is not running."
                    )
                    continue
                screen_agent.terminate_process()

            case _:
                print(f"{bcolors.RED}ERROR:{bcolors.ENDC} Invalid selection.")
print("Done.")
