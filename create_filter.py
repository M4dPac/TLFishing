import sys
import os
from threading import Thread
import mss
import numpy as np
import cv2
from loguru import logger
from time import time
from random import randint

from my_keyboard import tap_key, mouse_click, mouse_movement


monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080, "mon": 2}
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SHUTDOWN_PC = True  # выключение пк по завершении ловли
START_FISHING = False
GLOBAL_START = False
BLOCK_THREAD = False
COUNT_FISHING = 0

logger.remove()
logger.add(sys.stderr, level="INFO")
log_file_path = os.path.join(CURRENT_DIR, r"fishing.log")
logger.add(log_file_path, level="DEBUG")


def nothing(*args):
    pass


def setting_fishing_filter():

    with mss.mss() as sct:

        cv2.namedWindow("Result")
        cv2.namedWindow("Settings")

        cv2.createTrackbar("h1", "Settings", 0, 255, nothing)
        cv2.createTrackbar("s1", "Settings", 0, 255, nothing)
        cv2.createTrackbar("v1", "Settings", 0, 255, nothing)
        cv2.createTrackbar("h2", "Settings", 255, 255, nothing)
        cv2.createTrackbar("s2", "Settings", 255, 255, nothing)
        cv2.createTrackbar("v2", "Settings", 255, 255, nothing)

        while True:
            img = sct.grab(monitor)
            img = np.array(img)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # считываем значения бегунков
            h1 = cv2.getTrackbarPos("h1", "Settings")
            s1 = cv2.getTrackbarPos("s1", "Settings")
            v1 = cv2.getTrackbarPos("v1", "Settings")
            h2 = cv2.getTrackbarPos("h2", "Settings")
            s2 = cv2.getTrackbarPos("s2", "Settings")
            v2 = cv2.getTrackbarPos("v2", "Settings")

            # формируем начальный и конечный цвет фильтра
            h_min = np.array((h1, s1, v1), np.uint8)
            h_max = np.array((h2, s2, v2), np.uint8)

            # накладываем фильтр на кадр в модели HSV
            thresh = cv2.inRange(hsv, h_min, h_max)

            small_thresh = cv2.resize(thresh, (0, 0), fx=0.5, fy=0.5)

            cv2.imshow("Result", small_thresh)

            ch = cv2.waitKey(5)
            if ch == 27:
                break


def setting_fishing_screen():

    with mss.mss() as sct:

        cv2.namedWindow("Result")
        cv2.namedWindow("Settings")

        cv2.createTrackbar("x1", "Settings", 0, 1920, nothing)
        cv2.createTrackbar("y1", "Settings", 0, 1080, nothing)
        cv2.createTrackbar("x2", "Settings", 19920, 1920, nothing)
        cv2.createTrackbar("y2", "Settings", 1080, 1080, nothing)

        while True:
            img = sct.grab(monitor)
            img = np.array(img)

            # считываем значения бегунков
            x1 = cv2.getTrackbarPos("x1", "Settings")
            y1 = cv2.getTrackbarPos("y1", "Settings")
            x2 = cv2.getTrackbarPos("x2", "Settings")
            y2 = cv2.getTrackbarPos("y2", "Settings")

            cv2.imshow("Result", img[y1:y2, x1:x2])

            ch = cv2.waitKey(5)
            if ch == 27:
                break


def is_start_fishing(hsv) -> bool:
    # [594:709, 1101:1132]
    h = hsv.item(597, 1111, 0)
    return h <= 50


def check_bait(img) -> bool:
    logger.debug("Check bait")
    tmp_img = cv2.cvtColor(img[965:986, 904:932], cv2.COLOR_BGR2GRAY)
    file_path = os.path.join(CURRENT_DIR, r"images\empty_bait.png")
    template = cv2.imread(file_path, 0)

    res_template = cv2.matchTemplate(tmp_img, template, cv2.TM_CCOEFF_NORMED)
    min_value, max_value, min_location, max_location = cv2.minMaxLoc(res_template)

    threshold = 0.8
    res = max_value < threshold

    if res:
        logger.info("The bait is found")
    else:
        logger.info("The bait is not found")

    return res


def create_moments(img, thresh):
    moments = cv2.moments(thresh, 1)
    dM01 = moments["m01"]
    dM10 = moments["m10"]
    dArea = moments["m00"]

    if dArea > 100:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        cv2.circle(img, (x, y), 10, (0, 0, 255), -1)


def fishing(x, center):
    global BLOCK_THREAD

    BLOCK_THREAD = True

    if x < center:  # right
        tap_key("d")
    else:  # left
        tap_key("a")

    BLOCK_THREAD = False


def get_delay():
    return randint(8, 11)


def get_time(past_time):
    tmp = round(time() - past_time)
    hours = tmp // 3600
    minutes = tmp % 3600 // 60
    seconds = tmp % 3600 % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def get_image(sct):
    img = sct.grab(monitor)
    img = np.array(img)
    return img


def filter_hsv():
    global GLOBAL_START

    logger.info("Start program")

    x1, x2, y1, y2 = 666, 1248, 316, 419
    center = (x2 - x1) // 2
    fishing_count = 0
    fishing_start_time = None
    fishing_casting_time = None
    delay = get_delay()

    hsv_min = np.array((0, 33, 135), np.uint8)
    hsv_max = np.array((90, 255, 255), np.uint8)

    cv2.namedWindow("Result")
    with mss.mss() as sct:
        while True:

            img = get_image(sct)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            result_img = np.array(img)[y1:y2, x1:x2]
            fishing_img = np.array(hsv)[y1:y2, x1:x2]

            thresh = cv2.inRange(fishing_img, hsv_min, hsv_max)
            # small_thresh = cv2.resize(thresh, (0, 0), fx=0.5, fy=0.5)

            key = cv2.waitKey(1)
            match key:
                case 92:  # key \
                    break
                case 112:  # key p
                    text = ("Start fishing", "End fishing")[GLOBAL_START]
                    logger.info(text)
                    GLOBAL_START = not GLOBAL_START
                case _:
                    pass

            if GLOBAL_START:
                if fishing_start_time is None:
                    logger.info("Start counting time")
                    fishing_start_time = time()

                if fishing_casting_time is None:
                    logger.info("Set fishing_casting_time")
                    fishing_casting_time = time()

                start = is_start_fishing(hsv)

                if not start and (round(time() - fishing_casting_time) == delay):

                    if not check_bait(img):
                        x, y = randint(865, 932), randint(967, 987)
                        mouse_movement(x, y)
                        mouse_click()
                        x, y = randint(865, 932), randint(928, 949)
                        mouse_movement(x, y)
                        mouse_click()
                        x, y = randint(865, 1080), randint(928, 1250)
                        mouse_movement(x, y)
                        img = get_image(sct)

                    if not check_bait(img):
                        logger.info("Exit game")

                        tap_key("f10", 0.1)
                        mouse_movement(1532, 799)
                        mouse_click()
                        tap_key("y")
                        logger.info(f"Total time: {get_time(fishing_start_time)}")
                        logger.info(f"Casting count: {fishing_count}")

                        if SHUTDOWN_PC:
                            os.system("shutdown /s /t 20")
                        break

                    logger.info("Press key F")
                    tap_key("f")
                    fishing_count += 1

                if start:
                    # logger.info("Fishing")
                    moments = cv2.moments(thresh, 1)
                    dM01 = moments["m01"]
                    dM10 = moments["m10"]
                    dArea = moments["m00"]

                    if dArea > 20:
                        x = int(dM10 / dArea)
                        y = int(dM01 / dArea)
                        cv2.circle(result_img, (x, y), 10, (0, 0, 255), -1)

                        if not BLOCK_THREAD:
                            # fishing(x, center)
                            Thread(
                                target=fishing, args=(x, center), daemon=True
                            ).start()

                    fishing_casting_time = time()
                    delay = get_delay()

                for i, el in enumerate(
                    (
                        f"is_start: {start}",
                        f"Total time: {get_time(fishing_start_time)}",
                        f"Casting count: {fishing_count}",
                        f"Delay: {delay}",
                    ),
                    1,
                ):
                    cv2.putText(
                        result_img,
                        el,
                        (10, 15 * i),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        0.8,
                        (0, 0, 255),
                        1,
                        cv2.LINE_AA,
                    )
            else:
                fishing_start_time = None
                fishing_casting_time = None

            bgr_thresh = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
            combined_img = cv2.vconcat([result_img[:, :, :3], bgr_thresh])
            cv2.imshow("Result", combined_img)
            # cv2.imshow("Mask", thresh)
            # cv2.imshow("Result", small_thresh)

    cv2.destroyAllWindows()
    logger.info("End program")


if __name__ == "__main__":
    filter_hsv()
