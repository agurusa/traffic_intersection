from controller import consts
from controller.controller import Controller
import threading
import datetime as dt
from time import sleep
import random

"""
        [       ]          
        [       ]
        [       ]
--------         --------


--------         --------
        [       ]          
        [       ]
        [       ]
"""
HORIZ = '--------'
PADDING = '        '
VERT = f'[{PADDING}]'


def print_intersection():
    print(PADDING, VERT, PADDING)
    print(PADDING, VERT, PADDING)
    print(PADDING, VERT, PADDING)
    print(HORIZ, PADDING, HORIZ)
    print('\n')
    print(HORIZ, PADDING, HORIZ)
    print(PADDING, VERT, PADDING)
    print(PADDING, VERT, PADDING)
    print(PADDING, VERT, PADDING)


def add_traffic(lock, controller, timeout):
    now = dt.datetime.now()
    end = now + dt.timedelta(0, timeout)
    while dt.datetime.now() < end:
        with lock:
            direction = random.choices(consts.ORDER)[0]
            print(f'traffic in {direction}')
            ind = consts.ORDER.index(direction)
            controller.lanes[ind].cars.put(1)
        sleep(0.5)


def simulate(timeout):
    controller = Controller()
    now = dt.datetime.now()
    end = now + dt.timedelta(0, timeout)
    lock = threading.Lock()
    traffic = threading.Thread(target=add_traffic, daemon=True, args=(lock, controller, timeout))
    intersection = threading.Thread(target=controller.run, daemon=True, args=(timeout,))
    traffic.start()
    intersection.start()
    while dt.datetime.now() < end:
        with lock:
            _current = controller.current_lane
            print(f'light green: {_current.direction}')
            if not _current.cars.empty():
                _current.cars.get()
        sleep(consts.CAR_SPEED)

    intersection.join()
    traffic.join()


if __name__ == '__main__':
    print_intersection()
    simulate(10)
