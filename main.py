import csv
import math
import time

t_0 = time.time()
ideal_epoch_diff = 3600




arr_flights = []
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

passenger_data = {}

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
            passenger_data[int(row[0])] = -1
        
    



        
def bfs(dep, arr, global_start_time, start_time, iteration=0, max_iteration=3, gap_layover=ideal_epoch_diff):
    return_arr = []
    
    if iteration > max_iteration:
        return return_arr
    count = 0
    for i in dict_departures[dep]:
        path = []
        if i[ARR] == arr:
            if(i[1]>start_time):
                print(i[1], start_time, i[1]-start_time, i[3])
                path.append(i[0])
                return_arr.append(path)
        else:
            flight_end_time = i[2]
            count +=1
            # flight_end_time + gap_layover
            path.append(i[0])
            return_arr.extend(bfs(i[0], arr, 0, iteration+1, max_iteration, gap_layover))
    
    return return_arr
    
def dfs_2(dep, arr, start_time, passengers_commodity=-1, return_arr=[], path=[], iteration=0, max_iteration=3, gap_layover=ideal_epoch_diff):
    gl_passengers_commodity = passengers_commodity
    if iteration == 0:
        return_arr = []
        path = [dep]
        
    # if iteration==2:
    #     print("Error here")
    if iteration >= max_iteration:
        pass
    else:
        count = 0
        if(dep not in dict_departures):
            return
        for i in dict_departures[dep]:
            if i[0] in cancelled_flights:
                # pass
                continue
            if i[ARR] == arr:
                if(i[DEP_TIME]>start_time):
                    #print(i[1], start_time, i[1]-start_time, i[3])
                    new_path = path.copy()
                    new_path.append(i[FID])
                    new_path.append(i[ARR])
                    if(new_path==[8,28]):
                        print("HEREEE", passengers_commodity, i[CAPACITY]-i[BOOKED])
                    #new_path.append(i[ARR_TIME])
                    if(iteration!=0):
                        passengers_commodity = min(gl_passengers_commodity, i[CAPACITY]-i[BOOKED])
                    else:
                        passengers_commodity = i[CAPACITY]-i[BOOKED]
                        print("ALSO")
                    
                    #new_path.append(passengers_commodity)
                    return_arr.append([new_path, i[ARR_TIME], passengers_commodity])
            else:
                flight_end_time = i[ARR_TIME]
                # flight_end_time + gap_layover
                new_path = path.copy()
                new_path.append(i[FID])
                new_path.append(i[ARR])
                if(iteration!=0):
                    passengers_commodity = min(gl_passengers_commodity, i[CAPACITY]-i[BOOKED])
                else:
                    passengers_commodity = i[CAPACITY]-i[BOOKED]
                dfs_2(i[ARR], arr, flight_end_time+gap_layover,passengers_commodity, return_arr, new_path, iteration+1, max_iteration, gap_layover)
                #return_arr.extend(bfs(i[0], arr, 0, iteration+1, max_iteration, gap_layover))
        if iteration==0:
            return return_arr

def flight_rating_metric(num_layovers, time_diff, ideal_time_diff, capacity=0):
    time_diff = time_diff-ideal_time_diff
    if(time_diff<0):
        c = -1
    elif(time_diff==0):
        c = 0
    else:
        c = 1


    return 100*abs(time_diff)+10*num_layovers+c






def possible_routes(dep):
    routes = []
    for i in dict_departures[dep]:
        if i[0] in cancelled_flights:
            continue
        routes.append(i[ARR])
    return routes

def print_possible_routes(dep):
    for i in dict_departures[dep]:
        if i[0] in cancelled_flights:
            continue
        print(f"{dep}->{i[ARR]}")

def compute_min(flights):
    pt = []
    for i in range(len(flights)):
        #print(flights[i],":",arr_flights[flights[i]][CAPACITY]-arr_flights[flights[i]][BOOKED], end= ",")
        pt.append(arr_flights[flights[i]][CAPACITY]-arr_flights[flights[i]][BOOKED])
    return min(pt)


print(arr_flights[206][BOOKED], arr_flights[206][CAPACITY])



bked = 0
ov_data = {}
capacity_sums = []

for i in cancelled_flights:
    fid = i
    dep = arr_flights[i][DEP]
    arr = arr_flights[i][ARR]
    bked+=arr_flights[i][BOOKED]
    if dep == 8 and arr == 28:
        #print(f"Here is the BFS for {dep}, {arr}:", bfs_2(dep, arr, 0))
        pass
    data = []
    sum_total_capacity=0
    for i in dfs_2(dep, arr, 0, max_iteration=3):
        num_layouvers = (len(i[0])-1)/2
        time_diff = i[1]
        ideal_time_diff = arr_flights[fid][ARR_TIME]
        sum_total_capacity+=i[2]
        rating = flight_rating_metric(num_layouvers, time_diff, ideal_time_diff)
        data.append([i, rating])
        print(i)
    
    
    #print("SUM TOTAL CAPACITY:", sum_total_capacity)
    capacity_sums.append([sum_total_capacity, fid])
    left_unsorted = arr_flights[fid][BOOKED]
    #print("Stats:",arr, dep, left_unsorted)
    

    data = sorted(data, key=lambda x: x[1])
    
    ov_data[fid] = data
    
    
    for i in data:
        fids=[]
        for j in range(1, len(i[0][0]), 2):
            fids.append(i[0][0][j])
        #print(compute_min(fids))
        alloc = min(left_unsorted, compute_min(fids))
        for j in range(1, len(i[0][0]), 2):
            arr_flights[i[0][0][j]][BOOKED]+=alloc
            for k in range(left_unsorted-1, left_unsorted-alloc-1, -1):
                passenger_data[cancelled_passengers[fid][k]] = i[0][0]
            print(f"Allocating {alloc} passengers to flight {i[0][0][j]}")
        left_unsorted -= alloc
        if(left_unsorted==0):
            break
    
    
#capacity_sums = sorted(capacity_sums, key=lambda x: x[0])
# print(capacity_sums)
# for obj in capacity_sums:
#     fidd = obj[1]
#     data = ov_data[obj[1]]
#     #print("Data:", data)
    
#     for i in data:
#         fids=[]
#         for j in range(1, len(i[0][0]), 2):
#             fids.append(i[0][0][j])
#         #print(compute_min(fids))
#         alloc = min(left_unsorted, compute_min(fids))
#         for j in range(1, len(i[0][0]), 2):
#             arr_flights[i[0][0][j]][BOOKED]+=alloc
#             for k in range(left_unsorted-1, left_unsorted-alloc-1, -1):
#                 passenger_data[cancelled_passengers[fid][k]] = i[0][0]
#             print(f"Allocating {alloc} passengers to flight {i[0][0][j]}")
#         left_unsorted -= alloc
#         if(left_unsorted==0):
#             break
ppl_counter = 0
layover_counter = 0
with open('allot.csv', 'w') as f:
    
    for i in passenger_data.keys():
        if passenger_data[i] == -1:
            f.write(str(i)+',0\n')
            continue
        ppl_counter+=1
        row = []
        row.append(i)
        row.append(int((len(passenger_data[i])+1)/2 - 1))
        for j in range(1, len(passenger_data[i]), 2):
            row.append(passenger_data[i][j])
        layover_counter += row[1]
        f.write(','.join([str(i) for i in row])+'\n')

        

t_1 = time.time()

print("Total counter:", ppl_counter)
print("Total layover counter:", layover_counter)

print("Length of passenger data:",bked,len(passenger_data))    

with open('stats.csv', 'w') as f:
    f.write(f"Total passengers Affected: {bked}\n")
    f.write(f"Total reallocated: {ppl_counter}\n")
    f.write(f"Average layover: {layover_counter/ppl_counter}\n")
    f.write(f"Total time taken: {t_1-t_0}\n")


    





        

