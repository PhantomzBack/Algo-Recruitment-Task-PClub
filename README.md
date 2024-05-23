# Task 5 - Algorithms

## Instructions to run:
Simply run the following command
```py
python3 ./main.py
```


## Rough Logic:

The python file main.py contains the code. It uses modified DFS to an extent of 3 iterations account for a maximum of 3 layovers, and tries to discover the arrival airport of the flights that have been cancelled


## Designing the Metric for Choosing the Flight:

I needed a metric to decide the rating of a flight, and the parameters are

Since the priorities are given as 
1) The travel time should be as close as possible to the destination time
2) As less layovers as possible
3) Better earlier than later..

I didn't have a lot of time on hand to craft a better function so I have directly used 
$$F = abs(time\_diff)*100+num\_layovers*10 - signum(time_diff)$$
which is virtually just a handy way of saying _I want my most important factor to be the time, then num, and then higher priority to arriving earlier._ This function is not very realistic since ideally, it anyone would prefer to take one layover lesser but reach an insignifcant time earlier or later, but I used this for simplicity.


## Roadblocks: 

Since this is a real life scenario, an objective solution is hard to find. One of the main roadblocks I faced was deciding the order in which flights would be used for accomodation. My thought process was to try to maximize this even if it took more compute since there are many routes that use the same flight and so the flight ranking metric was used to sort through them to try to find the best flight suited for travel.

## Metric for Choosing A Better Solution:

Ideally, this is what we want
- The more the Passenger Satisfaction, the higher the metric function
- As many people re-allocated as possible, the better, so higher the metric function should be
- As many people from the same cancelled flight clubbed together into the same flight, the better, so again, the metric function should be higher. 

For a real life scenario it's not ideal to rank these in a strict order globally, and that's why a mathematical function would be better suited here too!









## verify.py

It's a script I created to ensure that the solutions follow constraints, in terms of overbooking


## Minimizing Number of Travels:


