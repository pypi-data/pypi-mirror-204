from pynput.mouse import Controller
import logging

def run():
    mouse = Controller()

    logger = logging.getLogger("apdaily_util")
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    while True:
        logger.info(mouse.position)