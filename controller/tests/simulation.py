import threading
import datetime as dt
import random
import argparse
from time import sleep

from controller import consts
from controller.controller import Controller

SHORT_PADDING = '    '
VERT= '|'
CAR = '*'
NEWLINE = '\n'
NO_CAR = ' '


class bcolors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BLUE = '\033[94m'


def print_intersection(lock, controller, timeout):
    now = dt.datetime.now()
    end = now + dt.timedelta(0, timeout)
    while dt.datetime.now() < end:
        with lock:
            greenlight = controller.current_lane.direction
            NS_T = controller.lanes[0].cars.qsize()
            NS_S = controller.lanes[1].cars.qsize()
            EW_T = controller.lanes[2].cars.qsize()
            EW_S = controller.lanes[3].cars.qsize()

        HORIZ = '-'*max(EW_T,EW_S, 15)
        PADDING = ' '*len(HORIZ)

        SOUTH_LANE = ''
        EAST_LANE_TURN = ''
        EAST_LANE_STRAIGHT = ''

        for i in range(max(NS_S, NS_T)):
            SOUTH_LANE += VERT
            SOUTH_LANE += CAR if i < NS_T else NO_CAR
            SOUTH_LANE += CAR if i < NS_S else NO_CAR
            SOUTH_LANE += VERT + NEWLINE

        for i in range(max(EW_S, EW_T)):
            EAST_LANE_STRAIGHT += CAR if i < EW_S else NO_CAR
            EAST_LANE_TURN += CAR if i < EW_T else NO_CAR

        while SOUTH_LANE.count(VERT) < len(HORIZ):
            SOUTH_LANE += VERT + NO_CAR + NO_CAR + VERT + NEWLINE

        while len(EAST_LANE_TURN) < len(HORIZ):
            EAST_LANE_TURN += NO_CAR

        while len(EAST_LANE_STRAIGHT) < len(HORIZ):
            EAST_LANE_STRAIGHT += NO_CAR


        HORIZ_TOP = EAST_LANE_TURN[::-1] + SHORT_PADDING + EAST_LANE_STRAIGHT
        HORIZ_BOTTON = EAST_LANE_STRAIGHT[::-1] + SHORT_PADDING + EAST_LANE_TURN


        NORTH_LANE = SOUTH_LANE[::-1]
        NORTH_SIDE = NEWLINE.join((PADDING + x for x in NORTH_LANE.split(NEWLINE)))
        SOUTH_SIDE = NEWLINE.join((PADDING + x for x in SOUTH_LANE.split(NEWLINE)))

        SOUTH_LIGHTS_TURN = f' {bcolors.GREEN}^{bcolors.ENDC}' if consts.SOUTH in greenlight[0] and consts.LEFT in greenlight[1] else f' {bcolors.RED}^{bcolors.ENDC}'
        SOUTH_LIGHTS_STRAIGHT = f'{bcolors.GREEN}^{bcolors.ENDC} ' if consts.SOUTH in greenlight[0] and consts.STRAIGHT in greenlight[1] else f'{bcolors.RED}^{bcolors.ENDC} '
        SOUTH_SIDE += SOUTH_LIGHTS_TURN + SOUTH_LIGHTS_STRAIGHT + NEWLINE + PADDING + f'{bcolors.BLUE}T,S {bcolors.ENDC} '

        HORIZ_TOP += f'{bcolors.GREEN}<{bcolors.ENDC}' if consts.EAST in greenlight[0] and consts.STRAIGHT in greenlight[1] else f'{bcolors.RED}<{bcolors.ENDC}'
        HORIZ_BOTTON += f'{bcolors.GREEN}<{bcolors.ENDC}' if consts.EAST in greenlight[0] and consts.LEFT in greenlight[1] else f'{bcolors.RED}<{bcolors.ENDC}'
        HORIZ_TOP += f'{bcolors.BLUE}S{bcolors.ENDC}'
        HORIZ_BOTTON += f'{bcolors.BLUE}T {bcolors.ENDC}'
        inters = [NORTH_SIDE, HORIZ + SHORT_PADDING + HORIZ, HORIZ_TOP, HORIZ_BOTTON, HORIZ + SHORT_PADDING + HORIZ, SOUTH_SIDE]
        for i in inters:
            print(i)

        sleep(0.1)


def add_traffic(lock, controller, timeout):
    now = dt.datetime.now()
    end = now + dt.timedelta(0, timeout)
    while dt.datetime.now() < end:
        with lock:
            direction = random.choices(consts.ORDER)[0]
            ind = consts.ORDER.index(direction)
            controller.lanes[ind].cars.put(1)
        sleep(consts.CAR_SPEED)


def simulate(timeout):
    controller = Controller()
    now = dt.datetime.now()
    end = now + dt.timedelta(0, timeout)
    lock = threading.Lock()
    visualize = threading.Thread(target=print_intersection, daemon=True, args=(lock, controller, timeout))
    traffic = threading.Thread(target=add_traffic, daemon=True, args=(lock, controller, timeout))
    intersection = threading.Thread(target=controller.run, daemon=True, args=(timeout,))
    visualize.start()
    traffic.start()
    intersection.start()
    while dt.datetime.now() < end:
        with lock:
            _current = controller.current_lane
            if not _current.cars.empty():
                _current.cars.get()
        sleep(consts.CAR_SPEED)

    visualize.join()
    intersection.join()
    traffic.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a traffic simulation')
    parser.add_argument(
        '--timeout',
        '-t',
        default=15,
        type=int,
        help='specify the amount of time you would like the simulation to run.')
    args = parser.parse_args()
    simulate(args.timeout)
