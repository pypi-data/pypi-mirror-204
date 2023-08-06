import os
import subprocess
import sys
import platform
from pynput import keyboard as kb
from pynput import mouse as ms
import time
import toml
import logging

def run():
    logger = logging.getLogger("apdaily_startup")
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    config = {}
    autosave = True

    logger.info("Launching Broswer")

    if platform.system() == "Linux":
        linux_config = toml.load("/usr/local/bin/apdaily/apdaily-config.toml")
        config = linux_config
        browser_prefix_path = str(config["startup-config"]["browser-prefix-path"])
        browser_executable = str(config["startup-config"]["browser-executable"])
        if not os.path.exists(os.path.join(browser_prefix_path, browser_executable)):
            logger.error("Browser not found")
            sys.exit(0)
        os.chdir(browser_prefix_path)
        os.system(f'gtk-launch {browser_executable} > /dev/null 2>&1 &')
    elif platform.system() == "Windows":
        windows_config = toml.load("C:\\Program Files\\apdaily-config.toml")
        browser_prefix_path = str(config["startup-config"]["browser-prefix-path"])
        browser_executable = str(config["startup-config"]["browser-executable"])
        if not os.path.exists(os.path.join(browser_prefix_path, browser_executable)):
            logger.error("Browser not found")
            sys.exit(0)
        subprocess.Popen(os.path.join(browser_prefix_path, browser_executable))
    else:
        logger.error("OS not supported")
        sys.exit(0)

    keyboard = kb.Controller()
    mouse = ms.Controller()

    url = str(config["startup-config"]["url"])

    time.sleep(5)

    STUDENT_SIGNIN = list(config["startup-config"]["student-signin"])
    NEXT = list(config["startup-config"]["next"])
    SIGNIN = list(config["startup-config"]["signin"])
    SELECTOR = list(config["startup-config"]["selector"])
    HUGE = list(config["startup-config"]["huge"])
    LEFT_SCROLL = list(config["startup-config"]["left-scroll"])
    MY_ASSIGNMENTS = list(config["startup-config"]["my-assignments"])
    ACTIVE = list(config["startup-config"]["active"])
    VIDEO_START_POS = list(config["startup-config"]["video-start-pos"])

    STUDENT_SIGNIN = (int(STUDENT_SIGNIN[0]), int(STUDENT_SIGNIN[1]))
    NEXT = (int(NEXT[0]), int(NEXT[1]))
    SIGNIN = (int(SIGNIN[0]), int(SIGNIN[1]))
    SELECTOR = (int(SELECTOR[0]), int(SELECTOR[1]))
    HUGE = (int(HUGE[0]), int(HUGE[1]))
    LEFT_SCROLL = (int(LEFT_SCROLL[0]), int(LEFT_SCROLL[1]))
    MY_ASSIGNMENTS = (int(MY_ASSIGNMENTS[0]), int(MY_ASSIGNMENTS[1]))
    ACTIVE = (int(ACTIVE[0]), int(ACTIVE[1]))
    VIDEO_START_POS = (int(VIDEO_START_POS[0]), int(VIDEO_START_POS[1]))

    def click():
        mouse.click(ms.Button.left)

    def enter():
        keyboard.press(kb.Key.enter)
        time.sleep(0.5)
        keyboard.release(kb.Key.enter)

    def enter_username():
        if not autosave:
            keyboard.type(str(config["credentials"]["username"]))
            time.sleep(0.5)
            enter()
            time.sleep(2)
        else:
            logger.info("Autosaving enabled, skipping username entry.")

    def enter_password():
        if not autosave:
            keyboard.type(str(config["credentials"]["password"]))
            time.sleep(0.5)
            enter()
            time.sleep(2)
        else:
            logger.info("Autosaving enabled, skipping username entry.")

    logger.info("Opening AP Classroom")
    keyboard.type(url)
    time.sleep(0.5)
    enter()
    time.sleep(5)
    logger.info("Signing in")
    mouse.position = STUDENT_SIGNIN
    time.sleep(3)
    click()
    time.sleep(2)
    enter_username()
    mouse.position = NEXT
    time.sleep(1)
    click()
    time.sleep(2)
    enter_password()
    mouse.position = SIGNIN
    time.sleep(2)
    click()
    time.sleep(15)
    mouse.position = SELECTOR
    time.sleep(1)
    click()
    time.sleep(1)
    mouse.position = HUGE
    time.sleep(1)
    click()
    time.sleep(3)
    mouse.position = LEFT_SCROLL
    time.sleep(0.5)
    mouse.scroll(0, -5)
    time.sleep(0.5)
    mouse.position = MY_ASSIGNMENTS
    time.sleep(0.5)
    click()
    time.sleep(0.5)
    mouse.position = ACTIVE
    time.sleep(0.5)
    click()
    time.sleep(3)
    mouse.position = VIDEO_START_POS
    logger.info("Startup Complete")










