# traffic_intersection
The code here addresses the task of **designing the control system for a 4 way traffic intersection.**

## Specifications
- There are 4 roads: (North, South, East, and West)
- There are two lanes per road: Through, and Left turn
- Each lane has a vehicle sensor and traffic light
- The intersection follows this cycle order: 
    * N, S: turn
    * N, S: through
    * E, W: turn
    * E, W: through
- Min and max wait times as follows:

Traffic pattern | Min (s) | Max (s)
---|---|---
N, S, Turn | 10 | 60
N, S, Through | 30 | 120
E, W, Turn | 10 | 30
E, W, Through | 30 | 60

- Optimize for throughput over wait time
- Light transition from Red to Green (no yellow)

## Design
### CONTROLLER 
The Controller object is responsible for the main logic of the intersection.

A Controller object has a:
- lanes array, containing all [Lane](#LANE) objects in the intersection.
- timer
- current lane
- next lane

#### Lanes array
The lanes are in the cycle order described in the [specifications](#Specifications). 
#### Timer
The timer keeps track of how long any one lane is active. This timer is reset when the controller switches to a new active lane.
#### Current Lane
The current lane indicates which lane is active (has a green light). The intersection is initialized by setting the North, South, Left lanes to green lights.
#### Next lane
The next lane indicates which lane has cars that are waiting, based on cycle order. If there are no cars in any intersection, next lane is simply the next lane in the cycle order. 

**_Examples_**

If North, South, Left is the `current lane`, and:
- There are no cars in N,S, Through
- There are cars in E,W, Left
- There are cars in E,W, Through
The `next lane` is E, W, Left.

If North, South, Left is the `current lane` and:
- There are no cars in N, S, Through
- There are no cars in E, W, Left
- There are no cars in E, W, Through
The `next lane` is N, S, Through

#### Run
Running the controller begins the logic that changes active lanes. 

- If the current lane has been active for the entirety of its maximum time, the next lane turns green, and the current lane turns red.
- If the current lane has no cars and another lane does have cars, the next lane turns green, and the current lane turns red.
- If no lane has cars (including the current lane), the current lane will stay green for its minimum time. The lane will turn red once its minimum time is reached, and the next lane will turn green.


### LANE
A Lane object has a:
- direction
- max time bound
- min time bounds
- light
- car queue
- sensor

#### Direction
The direction is one of the traffic patterns as described in the [specifications table](#Specifications). 
#### Max time bound
The max time bound the maximum amount of time any one lane of traffic is active. This means that the maximum amount of time a car in any lane would have to wait is the sum of all of the maximum time bounds: **4.5 minutes**. If there are no other lanes with traffic, and this lane's sensor has detected more cars, this lane will continue to be active. 
#### Min time bound
The min tme bound is the minimum amount of time any one lane is active, **if** there are no other lanes with traffic. If there is another lane with traffic, and this lane's sensor has not detected any other cars, this time bound is ignored.
#### Light
The light swaps the light color when the lane switches state. `OFF` is indicative of a red light, whereas `ON` indicates a green light.
#### Car queue
The queue holds all the traffic in the lane at the intersection. Note that the controller and lane objects do not know anything about this car queue, other than what can be determined by the sensor. This car queue is accessed directly by The [Real World](#The-Real-World) to add cars to different lanes, and remove cars from the active lane.
#### Sensor
The sensor cannot determine how many cars are in the car queue, and can only determine if the queue is empty. This is meant to emulate a single car sensor in a lane, which would only detect a single car at a time. 


### TIMER
A convenience class to keep track of the amount of time any one lane is active. 

### Known limitations
- If the current lane still has cars, but has reached the maximum time, **and** no other lanes have cars, the lane will briefly (1 second) turn red, before turning green again. 
- For simplicity, each lane is considered to be bidirectional. For example, one lane object holds the information for North, Through **and** South, Through. A second lane object holds the information for North, Turn **and** South, Turn. The [Real World](#The-Real-World) will not be able to add or remove cars to one lane in a single direction, but will combine the cars in both lanes. The sensor will thus determine if a car is in either lane (North, Through or South, Through), and the light will be turned on for both directions (North, South, Through).

## Testing
Tests can be run locally using `pytest`:
```shell script
# run tests
> python -m pytest

# output
controller/tests/test_controller.py::test_controller_init PASSED
controller/tests/test_controller.py::test_next_lane PASSED
controller/tests/test_controller.py::test_next_lane_with_traffic PASSED
controller/tests/test_controller.py::test_switch_lane PASSED
controller/tests/test_controller.py::test_waiting PASSED
controller/tests/test_controller.py::test_one_car_per_lane PASSED
controller/tests/test_controller.py::test_max_time PASSED

```
CircleCI is used for integration tests, and will run these pytests automatically after pushing commits.

These tests run 5 unit tests and two small simulations. 

### The Real World
To simulate and visualize the real world, please run `python -m controller.tests.simulation`. You can use the `--timeout` argument to specify the amount of time you'd like to run the simulation, or use the default (15 seconds). This will print a traffic intersection into the terminal window. You can see which lanes are active, and what cars are in the queue in real time. (Note that the intersection has color in standard zsh/terminal windows, and is NOT reflected accurately below). T = Turn, S = Straight, from the persepctive of South and East lanes.
```shell script
               |  |
               |  |
               | *|
               | *|
               | *|
               | *|
               | *|
               |**|
---------------    ---------------
              *    ****           <S
           ****    *              <T 
---------------    ---------------
               |**|
               |* |
               |* |
               |* |
               |* |
               |* |
               |  |
               |  |
                ^^ 
               T,S  
```

[simulation.py](controller/tests/simulation.py) indicates how the Control object can be instantiated and used to simulate traffic. Essentially:
```python
traffic = threading.Thread(target=add_traffic, daemon=True, args=(lock, controller, timeout))  # add traffic to lanes randomly
intersection = threading.Thread(target=controller.run, daemon=True, args=(timeout,))  # begin the controller logic
...
 _current = controller.current_lane
            if not _current.cars.empty():
                _current.cars.get()  # cars at the front of the lane drive off when the light is green
...

# from add_traffic
direction = random.choices(consts.ORDER)[0]
            ind = consts.ORDER.index(direction)
            controller.lanes[ind].cars.put(1)  # cars driving into the lane, waiting to get to the intersection

```
