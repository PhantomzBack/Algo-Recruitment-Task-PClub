import csv

arr_flights = []
ideal_eopch_diff = 3600
FID=0
DEP=1
ARR=2
CAPACITY = 3
DEP_TIME = 4
ARR_TIME = 5
BOOKED = 6
dict_departures = {}
cancelled_passengers = {}

with open('flights.csv', 'r') as f:
    reader = csv.reader(f)
    count=0
    for row in reader:
        if count == 0:
            count+=1
            continue
        flight_details = [int(i) for i in row]
        arr_flights.append(flight_details)
        arr_flights[int(row[0])].append(0)
        if(int(row[DEP]) not in dict_departures):
            dict_departures[int(row[DEP])] = [flight_details]#[[int(row[ARR]), int(row[DEP_TIME]), int(row[ARR_TIME]), int(row[FID])]]
        else:
            dict_departures[int(row[DEP])].append(flight_details)
        

cancelled_flights = []

with open('canceled.csv', 'r') as f:
    reader = csv.reader(f)
    count=0
    for row in reader:
        if count == 0:
            count+=1
            continue
        # print(row)
        cancelled_flights.append(int(row[0]))
        cancelled_passengers[int(row[0])] = []


with open('passengers.csv', 'r') as f:
    reader = csv.reader(f)
    count=0
    for row in reader:
        if count == 0:
            count+=1
            continue
        # print(row)
        arr_flights[int(row[1])][6]+=1
        if(int(row[1]) in cancelled_flights):
            cancelled_passengers[int(row[1])].append(int(row[0]))


with open('output.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        num_flights = int(row[1])
        for i in range(num_flights):
            flight = int(row[2+i])
            arr_flights[flight][BOOKED]+=1

for i in arr_flights:
    if i[BOOKED] > i[CAPACITY]:
        print("Overbooked:", i[FID])
    else:
        pass
        #print("All good")
            
            # if(flight_details[0] in cancelled_flights):
            #     cancelled_passengers[flight_details[0]].append(flight_details[1])