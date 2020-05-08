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
### LANE
A Lane object has a:
- direction
- max time bound
- min time bounds
- light
- car queue
- sensor

For simplicity, each lane is considered to be bidirectional. For example, one lane object holds the information for North, Through **and** South, Through. A second lane object holds the information for North, Turn **and** South, Turn. The Real World will not be able to add or remove cars to one lane in a single direction, but will combine the cars in both lanes. The sensor will thus determine if a car is in either lane (North, Through or South, Through), and the light will be turned on for both directions (North, South, Through). 

#### Direction
The direction is one of the traffic patterns as described in the [specifications table](#Specifications). 
#### Max time bound
The max time bound the maximum amount of time any one lane of traffic is active. This means that the maximum amount of time a car in any lane would have to wait is the sum of all of the maximum time bounds: **4.5 minutes**. If there are no other lanes with traffic, and this lane's sensor has detected more cars, this lane will continue to be active. 
#### Min time bound
The min tme bound is the minimum amount of time any one lane is active, **if** there are no other lanes with traffic. If there is another lane with traffic, and this lane's sensor has not detected any other cars, this time bound is ignored.
#### Light
The light swaps the light color when the lane switches state. `OFF` is indicative of a red light, whereas `ON` indicates a green light.
#### Car queue
The queue holds all the traffic in the lane at the intersection. Note that the controller and lane objects do not know anything about this car queue, other than what can be determined by the sensor. This car queue is accessed directly by The Real World to add cars to different lanes, and remove cars from the active lane.
#### Sensor
The sensor cannot determine how many cars are in the car queue, and can only determine if the queue is empty. This is meant to emulate a single car sensor in a lane, which would only detect a single car at a time. 


### TIMER
A convenience class to keep track of the amount of time any one lane is active. 