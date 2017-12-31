#!/usr/bin/env python

#Team Member Names:- Surbhi Paithankar, Sharad Ghule, Uteerna Koul
"""
Problem statement:- To find route, distance and time of path between two cities using various routing algorithms.

BFS Algorithm 
State Space - All cities reachable from the current city by road
Successor function- First element from the fringe
Goal State- Destination city
The program explores all neighboring cities using the concept of queue. The cost function has no effect on the output of the BFS.

DFS Algorithm 
State Space -All cities reachable from the current city by road
Successor function- Last element from the fringe
Goal State- Destination City
The program explores routes using the concept of stack. The cost function has no effect on the output of the BFS. This is the most inefficient algorithm as it explores a node till it doesn't find the goal city. So even if there is a direct route from the source to destination, the DFS algorithm never reaches till there.

Uniform Cost Search 
State Space - All cities reachable from the current city by road
Successor function- City with lowest distance to the next city
Goal State- Destination city
The algorithm determines the path by using a cost function. Priority Queue has been used to implement this algorithm.
1.Segments:
Edge weights- All edge weights are set to 1.
  In this case the priority is given to node with minimum segments. The cost of each segment is set to be 1. Therefore a node with minimum number of segment  s is explored.
2.Distance:
Edge weights- Distance between cities
  In this case the priority is given to the node with minimum value of distance. Therefore a node with minimum distance is explored. This gives the shortest distance to reach to the goal.
3.Time:
Edge weights- Time required to reach from one city to another. Calculated by distance(city,next city)/speedlimit(city,next city)
  In this case the priority is given to the node with minimum time required to reach the next node. The time is calculated dynamically by dividing distance   with speed limit of the segment.
Note - If the speed is unknown or equal to zero, the corresponding path is ignored by the algorithm
4.Longtour:
Edge weights- Distance between cities
  In this case the priority is given to the node with maximum value of distance. Therefore a node with maximum distance is explored. This is done by negating the priority.This gives the longest distance to reach to the goal.


PERFORMANCE ANALYSIS:
a.Routing Options:
  1.Distance- Astar seems to work the best, as it gives almost optimal result in shortest time.
  2.Time- Astar seems to work the best, as it gives almost fastest route in shortest time.
  3.Segments- In this case, BFS, Astar and Uniform have similar performances. There is no drastic difference observed.

b.Computation time:
  DFS gives the fastest results compared to other algorithms.
  For eg:- 
  time python route.py Benicia,_California Boston,_Massachusetts bfs distance
   Computation time = 8.347s
  time python route.py Benicia,_California Boston,_Massachusetts uniform distance
   Computation time = 8.42Sec
  time python route.py Benicia,_California Boston,_Massachusetts dfs distance
   Computation time = 3.8 sec only.
  time python route.py Benicia,_California Boston,_Massachusetts astar distance
   Computation time = 5.035 sec only.
 This proves that dfs has least computation time than all others.

c.Memory Requirement:
  DFS has least memory requirement. This is because of reduction of the explored state space.
  time python route.py Benicia,_California Boston,_Massachusetts bfs distance
   Total states explored = 5330
  time python route.py Benicia,_California Boston,_Massachusetts uniform distance
   Total states explored = 11244
  time python route.py Benicia,_California Boston,_Massachusetts astar distance
   Total states explored = 4878
  time python route.py Benicia,_California Boston,_Massachusetts dfs distance
   Total states explored = 4132
 This proves that dfs has lowest memory requirement than all others.

NOTE: Though DFS has least time and memory requirements, it gives the worst results amongst all the algorithms.


Astar HEURISTIC FUNCTION: 

1.Distance:
State Space - All cities reachable from the current city by road
Successor function- Element with lowest cost(n)+heuristic(n) value
Goal State- Destination city
Edge weights- Distance between cities

 Heuristic function: Distance of a city from the goal city. This distance has been calculated using the great circle distance between the latitude & longitu de of cities. 
 The function is admissible because it would always calculate the shortest distance of reaching from a city to the goal city. Hence it will always direct us towards the shortest route for reaching the goal city.
 Cost function: Total distance travelled till now.
 Using the above-mentioned h(n) and c(n), the state space was reduced to more than half and hence results in better performance.

2.Segments:
State Space - All cities reachable from the current city by road
Successor function- Element with lowest cost(n)+heuristic(n) value
Goal State- Destination city
Edge weights- All edge weights are set to 1.

 Heuristic function: Least number of edge required to reach from a city to the goal city. This is set to 1.
 The function is admissible because it would always have least number of segment for reaching from a city to the goal city i.e 1. Hence it will always direc t us towards the route with least edges for reaching the goal city.
 Cost function: Total number of edges travelled till now.

3.Time:
State Space - All cities reachable from the current city by road
Successor function- Element with lowest cost(n)+heuristic(n) value
Goal State- Destination city
Edge weights- Time required to reach from one city to another. Calculated by distance(city,next city)/speedlimit(city,next city)
 Heuristic function: Least amount of time required to reach to the goal city. The time has been calculated by dividing the distance(city,goal)/speed(city,g  oal) 
 Distance(city,goal)= Calculated using the great circle distance between the latitude & longitude of cities. 
 Speed(city,goal) is assumed to be same as speed(city,next_city)
 The function is admissible because it would always calculate the least time for reaching from a city to the goal city. Hence it will always direct us towar ds the route for goal city which requires minimal time.
 Cost function . Total time travelled till now.
 Using the above-mentioned h(n) and c(n), the state space was reduced to more than half and hence results in better performance.

4.Longtour:
State Space - All cities reachable from the current city by road
Successor function- Element with lowest cost(n)+heuristic(n) value
Goal State- Destination city
Edge weights- Distance between cities
  In this case the priority is given to the node with maximum value of distance. Therefore a node with maximum distance is explored. This is done by negating the value of h(n)+c(n). h(n) & c(n) are calculate as similar to the distance cost function of astar. Howver they are negated later, in order to fetch the one with highest value using priority queue.This gives the longest distance to reach to the goal.

ASSUMPTIONS:
1. If the speed of a segment is unknown or equal to zero, the path is ignored.
2. In case of highway intersections, we do not have their corresponding latitudes and longitudes available. Therefore for heuristic calculation, we assume     that the highway intersection always lies in the path towards the goal.
   Therefore,Dist(highway_intersection,goal)=dist(previous_city,goal)-dist(previous_city,highway_intersection)

IMPROVEMENT:
We observe that the result obtained by the astar is close to optimal but not equal. This is because using this heuristic we are estimating the distance of the highway intersections from the goal. This results in such tradeoff. 

CITATIONS:
Great Circle Distance - https://en.wikipedia.org/wiki/Great-circle_distance

"""


import sys
import Queue
import math

segmentfile = "road-segments.txt"
cityfile = "city-gps.txt"

citydir = {}
total_distance = 0

with open(segmentfile,"r") as myfile:
    segmentlist = [line.rstrip('\n') for line in myfile]
rsegment = [i.split(" ") for i in segmentlist]

with open(cityfile,"r") as cfile:
    clist = [line.rstrip('\n') for line in cfile]
citydata = [i.split(" ") for i in clist]

#Store corresponding lattitude and longitude of every city in a directory
for city in citydata:
    citydir[city[0]] = [city[1],city[2]]

#Store names of all US states 
USstate = ['Mississippi', 'Iowa', 'Oklahoma', 'Wyoming', 'Minnesota', 'New_Jersey', 'Arkansas', 'Indiana', 'Maryland', 'Louisiana', 'New_Hampshire', 'Texas', 'New_York', 'Arizona', 'Wisconsin', 'Michigan', 'Kansas', 'Utah', 'Virginia', 'Oregon', 'Connecticut', 'Montana', 'California', 'Idaho', 'New_Mexico', 'South_Dakota', 'Massachusetts', 'Vermont', 'Georgia', 'Pennsylvania', 'Florida', 'North_Dakota', 'Tennessee', 'Nebraska', 'Kentucky', 'Missouri', 'Ohio', 'Alabama', 'Illinois', 'Colorado', 'Washington', 'West_Virginia', 'South_Carolina', 'Rhode_Island', 'North_Carolina', 'Nevada', 'Delaware', 'Maine']

#Checks if a city is in US
def isUScity(city):
    city = city.split('_')
    state = city[len(city)-1]
    if state in USstate:
        return 1
    else:
        return 0    

#Calculate distance between two cities using latitude and longitude points. 
#Great circle distance has been employed.
def calc_distance(lat1,long1,lat2,long2):
    radian_constant = 0.0174533
    lat1_rad = float(lat1) * radian_constant
    lat2_rad = float(lat2) * radian_constant
    long1_rad = float(long1) * radian_constant
    long2_rad = float(long2) * radian_constant
    radius = 3959
    diff_long = long1_rad - long2_rad
    delta =  math.acos(math.sin(lat1_rad)*math.sin(lat2_rad)+math.cos(lat1_rad)*math.cos(lat2_rad)*math.cos(diff_long))
    distance = radius * delta
    return distance

# Construction of list from the road-segments to store speed information
tgraph = {}
for city in rsegment:
    if city[0] in tgraph.keys():
        tgraph[city[0]][city[1]]=[city[2],city[3],city[4]]
        if city[1] not in tgraph.keys():
            tgraph[city[1]]={}
            tgraph[city[1]][city[0]]=[city[2],city[3],city[4]]
        else:
            tgraph[city[1]][city[0]]= [city[2],city[3],city[4]]
    else:
        tgraph[city[0]]={}
        tgraph[city[0]][city[1]]=[city[2],city[3],city[4]]
        if city[1] not in tgraph.keys():
            tgraph[city[1]]={}
            tgraph[city[1]][city[0]]=[city[2],city[3],city[4]]
        else:
            tgraph[city[1]][city[0]]= [city[2],city[3],city[4]]
        
#Function implements BFS Algorithm to find path
#The program explores all neighboring cities using the concept of queue. The cost function has no effect on the output of the BFS.
def BFS():
    if cost_function == "segments" or cost_function == "distance" or  cost_function == "time" or cost_function=="longtour":
        BFSqueue = []
        BFSqueue.append((source_city,source_city))
        visited1=[]
        track = source_city
        while len(BFSqueue)>0:
            current_city,track = BFSqueue.pop(0)
            for reachable_city in tgraph[current_city]:
                if reachable_city == dest_city:
                    print "Number of Visited nodes: ",len(visited1)
                    return (track+' '+reachable_city)
                else:
                    if reachable_city not in visited1 and current_city not in visited1 and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:
                        BFSqueue.append((reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)

        print "Sorry no route found"            
    else:
        print "Please enter valid cost function"

"""
Uniform Cost Search - The algorithm determines the path by using a cost function. Priority Queue has been used to implement this algorithm.
1.Segments:
In this case the priority is given to node with minimum segments. The cost of each segment is set to be 1. Therefore a node with minimum number of segments is explored.
2.Distance:
In this case the priority is given to the node with minimum value of distance. Therefore a node with minimum distance is explored. This gives the shortest distance to reach to the goal.
3.Time:
 In this case the priority is given to the node with minimum time required to reach the next node. The time is calculated dynamically by dividing distance with speed limit of the segment.
Note . If the speed is unknown or equal to zero, the corresponding path is ignored by the algorithm
"""

def UCF():

    if cost_function == "segments":

        UCFqueue = Queue.PriorityQueue()
        UCFresult = Queue.LifoQueue()
        track = []
        current_city = source_city
        visited1 = []
        total_segments = 0
        if source_city==dest_city:
            print "length ",len(visited1)
            return track.append(source_city)
        UCFqueue.put((0,source_city,source_city))

        while not UCFqueue.empty():
            total_segments, current_city, track = UCFqueue.get()
            if current_city==dest_city:
                print "Number of Visited nodes: ",len(visited1)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited1 and current_city not in visited1:
                    if tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:
                        UCFqueue.put(((int(total_segments)+1),reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)
        print "Sorry no route found"

    elif cost_function == "distance":

        UCFqueue = Queue.PriorityQueue()
        UCFresult = Queue.LifoQueue()
        track = []
        current_city = source_city
        visited1 = []

        if source_city==dest_city:
            print "Number of Visited nodes: ",len(visited1)
            return track.append(source_city)
        UCFqueue.put((0,source_city,source_city))

        while not UCFqueue.empty():
            cost, current_city, track = UCFqueue.get()
            #visited1.append(current_city)
            if current_city==dest_city:
                print "length ",len(visited1)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited1 and current_city not in visited1 and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:
                    val = int(tgraph[current_city][reachable_city][0])+cost
                    UCFqueue.put((val,reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)
        print "Sorry no route found"

        
    elif cost_function == "longtour":
        
        UCFqueue = Queue.PriorityQueue()
        UCFresult = Queue.LifoQueue()
        track = []
        current_city = source_city
        visited1 = []
        
        if source_city==dest_city:
            print "Number of Visited nodes: ",len(visited1)
            return track.append(source_city)
        UCFqueue.put((0,source_city,source_city))

        while not UCFqueue.empty():
            cost, current_city, track = UCFqueue.get()
            cost = -1 * cost
            #visited1.append(current_city)
            if current_city==dest_city:
                print "length ",len(visited1)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited1 and current_city not in visited1 and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:
                    val = -(int(tgraph[current_city][reachable_city][0])+cost)
                    UCFqueue.put((val,reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)
        print "Sorry no route found"

    elif cost_function == "time":
        visited1 = []
        UCFqueue = Queue.PriorityQueue()
        UCFresult = Queue.LifoQueue()
        track = []
        current_city = source_city

        if source_city==dest_city:
            return track.append(source_city)
        UCFqueue.put((0,source_city,source_city))

        while not UCFqueue.empty():
            total_time, current_city, track = UCFqueue.get()
            if current_city==dest_city:
                print "Number of Visited nodes: ",len(visited1)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited1 and current_city not in visited1 and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:

                    distance = int(tgraph[current_city][reachable_city][0])
                    speed =  int(tgraph[current_city][reachable_city][1])
                    if speed!=0 :
                        time = float(distance)/float(speed)
                        UCFqueue.put(((time+total_time),reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)
        print "Sorry no route found"

    else:
        print "Kindly enter valid cost function."

"""
Function to implement the astar algorithm.
"""
def astar():

    if cost_function == "segments":

        UCFqueue = Queue.PriorityQueue()
        UCFresult = Queue.LifoQueue()
        track = []
        current_city = source_city
        visited1 = []
        total_segments = 0
        heu = 1
        if source_city==dest_city:
            print "length ",len(visited1)
            return track.append(source_city)
        UCFqueue.put((0+heu,0,source_city,source_city))

        while not UCFqueue.empty():
            heufunc,total_segments, current_city, track = UCFqueue.get()
            if current_city==dest_city:
                print "Number of Visited nodes: ",len(visited1)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited1 and current_city not in visited1 and tgraph[reachable_city][current_city][1]!=''and int(tgraph[reachable_city][current_city][1])>0:
                    seg = int(total_segments)+1
                    UCFqueue.put((seg+heu,seg,reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)
        print "Sorry no route found"

    elif cost_function == "distance":
        visited=[]
        UCFqueue = Queue.PriorityQueue()
        track = []
        heu = calc_distance(citydir[source_city][0],citydir[source_city][1],citydir[dest_city][0],citydir[dest_city][1])
        heuristic = {}
        heuristic[source_city] = heu
        current_city = source_city
        i=0
        cost = 0
        if source_city==dest_city:
            return track.append(source_city)
        UCFqueue.put((cost+heu,cost,source_city,source_city))

        while not UCFqueue.empty():
    
            heufunc,cost, current_city, track = UCFqueue.get()
            if current_city==dest_city:
                print "Number of Visited nodes: " , len(visited)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited and current_city not in visited and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:

                    cost_new = cost + float(tgraph[current_city][reachable_city][0])
                    if (reachable_city in citydir.keys()):                        
                        heu = calc_distance(citydir[reachable_city][0],citydir[reachable_city][1],citydir[dest_city][0],citydir[dest_city][1])
                        UCFqueue.put(((heu + cost_new),cost_new,reachable_city,(track + ' ' + reachable_city)))                    
                    else:
                        heu = heuristic[current_city]
                        heu = heu - int(tgraph[current_city][reachable_city][0])
                        UCFqueue.put(((heu + cost_new),cost_new,reachable_city,(track + ' '+ reachable_city)))
                    heuristic[reachable_city] = heu
            visited.append(current_city)
        print "Sorry no route found"

    elif cost_function == "longtour":
        visited=[]
        UCFqueue = Queue.PriorityQueue()
        track = []
        heu = calc_distance(citydir[source_city][0],citydir[source_city][1],citydir[dest_city][0],citydir[dest_city][1])
        heuristic = {}
        heuristic[source_city] = heu
        current_city = source_city
        i=0
        cost = 0
        if source_city==dest_city:
            return track.append(source_city)
        UCFqueue.put((cost+heu,cost,source_city,source_city))

        while not UCFqueue.empty():

            heufunc,cost, current_city, track = UCFqueue.get()
            if current_city==dest_city:
                print "Number of Visited nodes: " , len(visited)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited and current_city not in visited and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:

                    cost_new = cost + float(tgraph[current_city][reachable_city][0])
                    if (reachable_city in citydir.keys()):
                        heu = calc_distance(citydir[reachable_city][0],citydir[reachable_city][1],citydir[dest_city][0],citydir[dest_city][1])
                        UCFqueue.put((((heu + cost_new)*-1),cost_new,reachable_city,(track + ' ' + reachable_city)))
                    else:
                        heu = heuristic[current_city]
                        heu = heu - int(tgraph[current_city][reachable_city][0])
                        UCFqueue.put((((heu + cost_new)*-1),cost_new,reachable_city,(track + ' '+ reachable_city)))
                    heuristic[reachable_city] = heu
            visited.append(current_city)

        print "Sorry no route found"

    elif cost_function == "time":
        visited1 = []
        UCFqueue = Queue.PriorityQueue()
        UCFresult = Queue.LifoQueue()
        track = []
        current_city = source_city
        heuristic = {}
        heuristic[source_city] = calc_distance(citydir[source_city][0],citydir[source_city][1],citydir[dest_city][0],citydir[dest_city][1])

       
        if source_city==dest_city:
            return track.append(source_city)
        UCFqueue.put((0,0,0,source_city,source_city))

        while not UCFqueue.empty():
            heu_func,total_time,cur_distance, current_city, track = UCFqueue.get()
            if current_city==dest_city:
                print "Number of Visited nodes: ",len(visited1)
                return track
            for reachable_city in tgraph[current_city]:
                if reachable_city not in visited1 and current_city not in visited1 and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:


                    distance = int(tgraph[current_city][reachable_city][0])
                    total_distance = distance+cur_distance

                    speed =  int(tgraph[current_city][reachable_city][1])
                    if speed==0 :
                        break
                    time = float(distance)/float(speed)
                    cur_time = time+total_time

                    avg_speed = float(total_distance /(cur_time))

                    if (reachable_city in citydir.keys()):
                        heu = calc_distance(citydir[reachable_city][0],citydir[reachable_city][1],citydir[dest_city][0],citydir[dest_city][1])
                    else:
                        heu = heuristic[current_city]
                        heu = heu - int(tgraph[current_city][reachable_city][0])
                    heu_value = float(heu/speed)
                    heuristic[reachable_city] = heu
                    UCFqueue.put((heu_value+cur_time,(cur_time),total_distance,reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)
    

#Function implements DFS Algorithm to find path
"""
DFS Algorithm- The program explores routes using the concept of stack. The cost function has no effect on the output of the BFS. This is the most inefficient algorithm as it explores a node till it doesn.t find the goal city. So even if there is a direct route from the source to destination, the DFS algorithm never reaches till there.

"""
def DFS():
    if cost_function == "segments" or cost_function == "distance" or  cost_function == "time" or cost_function =="longtour":
        DFSqueue = []
        DFSqueue.append((source_city,source_city))
        visited1=[]
        track = source_city
        while len(DFSqueue)>0:
            current_city,track = DFSqueue.pop()
            for reachable_city in tgraph[current_city]:
                if reachable_city == dest_city:
                    print "Number of Visited nodes: ",len(visited1)
                    return (track+' '+reachable_city)
                else:
                    if reachable_city not in visited1 and current_city not in visited1 and tgraph[reachable_city][current_city][1]!='' and  int(tgraph[reachable_city][current_city][1])>0:

                        DFSqueue.append((reachable_city,(track+' '+reachable_city)))
            visited1.append(current_city)

        print "Sorry no route found"
    else:
        print "Please enter valid cost function"

#Prints the final path and also calculates the total distance and time along the path. 
def print_path(track):

    path = []
    final_path = ""
    path = track.split(" ")
    total_distance = 0
    total_time = 0
    time_segment = 0
    distance_segment = 0
    speed_segment = 0
    total_speed = 0
    i=0
    print "City","->","Next city","->","Distance","->","Speed Limit","->","Highway Name"
    while i<len(path):
        if i!=len(path)-1:
            distance_segment= float(tgraph[path[i]][path[i+1]][0])
            speed_segment = float(tgraph[path[i]][path[i+1]][1])
            if speed_segment!=0:
                time_segment = float(distance_segment / speed_segment)
            total_time += time_segment
            total_distance += distance_segment
            print path[i],"->",path[i+1],"->",round(distance_segment,0),"->",round(speed_segment,0),"->",tgraph[path[i]][path[i+1]][2]
            if i>=1:
                final_path = path[i]+' '+final_path
        i = i+1

    print total_distance,round(total_time,4),path[0],final_path,path[(len(path)-1)]
        
        
 
#Accept the source & dest city, algorithm and the cost function from the user.                
source_city = str(sys.argv[1])
dest_city = str(sys.argv[2])
algorithm = str(sys.argv[3])
cost_function = str(sys.argv[4])

if source_city not in citydir.keys() or dest_city not in citydir.keys():
    print "Please enter valid source/destination cities."
else:
    #Chooses the algorithm according the given input parameter and cost function
    if algorithm == "bfs" :
        track =BFS()
    elif algorithm == "uniform":     
        track = UCF()
    elif algorithm == "astar":
        track = astar()
    elif algorithm == "dfs":
        track = DFS()
    else:
        print "Please enter valid algorithm."
        track = []
#Prints final track
    if(track):
        print_path(track)
