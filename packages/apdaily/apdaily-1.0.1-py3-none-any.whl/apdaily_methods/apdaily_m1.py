from pynput.mouse import Controller, Button
import time
import logging
import toml
import platform
import os
import sys

def run():
    mouse = Controller()

    logger = logging.getLogger("apdaily_main")
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    config = {}

    if platform.system() == "Linux":
        linux_config = toml.load("/usr/local/bin/apdaily/apdaily-config.toml")
        config = linux_config
    elif platform.system() == "Windows":
        windows_config = toml.load("C:\\Program Files\\apdaily\\apdaily-config.toml")
        config = windows_config
    else:
        logger.error("OS not supported")
        sys.exit(0)

    TOTAL_VIDEO_COUNT = int(config["main-config"]["total-video-count"])

    SETTINGS = list(config["main-config"]["settings"])
    DOUBLE_SPEED = list(config["main-config"]["double-speed"])
    PLAY = list(config["main-config"]["play"])
    EXIT = list(config["main-config"]["exit"])

    SETTINGS = (int(SETTINGS[0]), int(SETTINGS[1]))
    DOUBLE_SPEED = (int(DOUBLE_SPEED[0]), int(DOUBLE_SPEED[1]))
    PLAY = (int(PLAY[0]), int(PLAY[1]))
    EXIT = (int(EXIT[0]), int(EXIT[1]))

    def convert(wait_times):
        out = []
        for str_time in wait_times:
            time_list = str_time.split(":")
            out_time = int(time_list[0]) * 60 + int(time_list[1])
            out.append(out_time)
        return out

    def get_converted_wait_times():
        wait_times = config["main-config"]["wait-times"]
        return convert(wait_times)

    WAIT_TIMES = get_converted_wait_times()

    def countdown(t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

    def move_down():
        mouse.move(0, (1.0/12.0))

    def scroll_down():
        mouse.scroll(0, -1)
        move_down()

    def wait(index=-1, t=0.5):
        if index == -1:
            time.sleep(t)
        else:
            time.sleep(WAIT_TIMES[index])

    def double_speed():
        mouse.position = SETTINGS
        wait(t=2)
        mouse.click(button=Button.left)
        wait(t=2)
        mouse.position = DOUBLE_SPEED
        wait(t=2)
        mouse.click(button=Button.left)
        wait(t=1)
        mouse.click(button=Button.left)


    def play_video(index):
        mouse.click(button=Button.left)
        wait(t=3)
        double_speed()
        wait(t=2)
        mouse.position = PLAY
        wait()
        mouse.click(button=Button.left)
        wait()
        countdown(WAIT_TIMES[index])
        exit_video()
        move_down()

    def exit_video():
        mouse.position = EXIT
        wait()
        mouse.click(button=Button.left)
        wait()

    time.sleep(1)

    for i in range(TOTAL_VIDEO_COUNT-1):
        play_video(i)
        exit_video()
        scroll_down()
        time.sleep(0.5)
        logger.info(f"Video {i+1} done")

    logger.info("Move down with correction")
    time.sleep(2)
    scroll_down()
    time.sleep(1)

    mouse.move(0, 70)
    time.sleep(0.5)
    mouse.move(0, 80)
    time.sleep(0.5)
    mouse.move(0, 80)
    time.sleep(0.5)
    mouse.move(0, 100)
    time.sleep(0.5)
    scroll_down()
    time.sleep(0.5)
    mouse.move(0, 10)

