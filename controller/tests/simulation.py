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

        horizontal = '-'*max(EW_T, EW_S, 15)
        padding = ' '*len(horizontal)

        south_lane = east_lane_turn = east_lane_straight = ''

        for i in range(max(NS_S, NS_T)):
            south_lane += VERT
            south_lane += CAR if i < NS_T else NO_CAR
            south_lane += CAR if i < NS_S else NO_CAR
            south_lane += VERT + NEWLINE

        for i in range(max(EW_S, EW_T)):
            east_lane_straight += CAR if i < EW_S else NO_CAR
            east_lane_turn += CAR if i < EW_T else NO_CAR

        while south_lane.count(VERT) < len(horizontal):
            south_lane += VERT + NO_CAR + NO_CAR + VERT + NEWLINE

        while len(east_lane_turn) < len(horizontal):
            east_lane_turn += NO_CAR

        while len(east_lane_straight) < len(horizontal):
            east_lane_straight += NO_CAR

        horiz_top = east_lane_turn[::-1] + SHORT_PADDING + east_lane_straight
        horiz_bottom = east_lane_straight[::-1] + SHORT_PADDING + east_lane_turn

        north_lane = south_lane[::-1]
        north_side = NEWLINE.join((padding + x for x in north_lane.split(NEWLINE)))
        south_side = NEWLINE.join((padding + x for x in south_lane.split(NEWLINE)))

        south_lights_turn = f' {bcolors.GREEN}^{bcolors.ENDC}' if consts.SOUTH in greenlight[0] and consts.LEFT in greenlight[1] else f' {bcolors.RED}^{bcolors.ENDC}'
        south_lights_straight = f'{bcolors.GREEN}^{bcolors.ENDC} ' if consts.SOUTH in greenlight[0] and consts.STRAIGHT in greenlight[1] else f'{bcolors.RED}^{bcolors.ENDC} '
        south_side += south_lights_turn + south_lights_straight + NEWLINE + padding + f'{bcolors.BLUE}T,S {bcolors.ENDC} '

        horiz_top += f'{bcolors.GREEN}<{bcolors.ENDC}' if consts.EAST in greenlight[0] and consts.STRAIGHT in greenlight[1] else f'{bcolors.RED}<{bcolors.ENDC}'
        horiz_bottom += f'{bcolors.GREEN}<{bcolors.ENDC}' if consts.EAST in greenlight[0] and consts.LEFT in greenlight[1] else f'{bcolors.RED}<{bcolors.ENDC}'
        horiz_top += f'{bcolors.BLUE}S{bcolors.ENDC}'
        horiz_bottom += f'{bcolors.BLUE}T {bcolors.ENDC}'

        inters = [north_side, horizontal + SHORT_PADDING + horizontal, horiz_top, horiz_bottom, horizontal + SHORT_PADDING + horizontal, south_side]
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
