#!/usr/local/bin/python3
# route.py
# Code by: [ Naga Anjaneyulu - nakopa , Ruthvik parvataneni -rparvat,Prudhvi Vajja - pvajja ]
# put your routing program here!

from queue import PriorityQueue
import math
import sys

class city:
    
    def __init__(self,city_state,state,latitude,longitude):
        self.city_state = city_state
        self.state = state
        self.latitude = latitude
        self.longitude = longitude
    
    def get_name(self):
        return self.city_state
    def get_state(self):
        return self.state
    def get_latitude(self):
        return self.latitude
    def get_longitude(self):
        return self.longitude
    def set_latitude(self,latitude):
        self.latitude = latitude
    def set_longitude(self,longitude):
        self.longitude = longitude
        
        
        
class route:
    
    def __init__(self,from_city_state,to_city_state,distance,speed,highway):
        self.from_city_state = from_city_state
        self.to_city_state = to_city_state
        self.distance = distance
        self.speed = speed
        self.highway = highway
        
    def get_from_name(self):
        return self.from_city_state
    
    def get_to_name(self):
        return self.to_city_state
    def get_distance(self):
        return self.distance
    def get_speed(self):
        return self.speed
    def get_highway(self):
        return self.highway

class road_network:

    def __init__(self,cities,routes):
        self.cities = cities
        self.routes = routes
        
    def build_netwrok(self):
        road_network =  {}
        for city in self.cities:
            city_name = city.get_name()
            for route in self.routes:
                from_city_state = route.get_from_name()
                if city_name == from_city_state:
                    if city_name not in road_network.keys():
                        road_network[city_name] = {"city" : city , "routes" :[route]}
                    elif city_name in road_network.keys():
                        road_network[city_name]["routes"].append(route)
        return road_network
    
    def get_cities(self):
        return self.cities
    def get_routes(self):
        return self.routes

                
    
def compute_lat_long(ranges,from_city,curr_city,graph,recursion_depth):
    routes = graph[curr_city]["routes"]
    lat_wavg = []
    long_wavg = [] 
    cumm_dist = 0
    for route in routes:
        if route.get_to_name() != from_city and recursion_depth <= 5:
            neighbour_city = graph[route.get_to_name()]["city"]
            lat = neighbour_city.get_latitude()
            long = neighbour_city.get_longitude()
            if(lat == -1 and long == -1) :
                lat,long = compute_lat_long(ranges,curr_city,neighbour_city.get_name(),graph,recursion_depth+1)  
            distance = route.get_distance()
            cumm_dist += distance
            lat_wavg.append(distance*lat)
            long_wavg.append(distance*long)
    if cumm_dist > 0:
        return (sum(lat_wavg)/cumm_dist),(sum(long_wavg)/cumm_dist)
    else:
        return ranges[0],ranges[1]




def compute_distance(ranges,curr_city,end_city,graph):
    curr_lat = curr_city.get_latitude()
    curr_long = curr_city.get_longitude()
    end_lat = end_city.get_latitude()
    end_long = end_city.get_longitude()
    if curr_lat == -1 and curr_long == -1:
        curr_lat,curr_long = compute_lat_long(ranges,"",curr_city.get_name(),graph,0)
    elif end_lat == -1 and end_long == -1 :
        end_lat,end_long = compute_lat_long(ranges,"",end_city.get_name(),graph,0)
        

    """
    The distance between two latitude and longitude positions is calculated using
    haversine formula , which we have referred from Math Forum
    
    @ref : http://mathforum.org/library/drmath/view/51879.html
    
    """
    dlat = math.radians(end_lat - curr_lat)
    dlong = math.radians(end_long - curr_long)
    a = math.pow(math.sin(dlat/2),2) + (math.cos(curr_city.get_latitude())*
                 math.cos(end_city.get_latitude())*math.pow(math.sin(dlong/2),2))
    c = 0
    if a >= 0 :
        c = 2*math.asin(min(1,math.sqrt(a)))
    else: c = 2*math.asin(min(1,-math.sqrt(abs(a))))
    " Earth radius in miles"
    R = 3956
    return  R*c

def compute_time(curr_city,dist,graph):
    routes = graph[curr_city]["routes"]
    max_speed =0
    for route in routes:
        speed = route.get_speed()
        if( speed > max_speed ):
            max_speed = speed
     
    return dist/max_speed
    
    
def compute_mpg(curr_city,graph):
    routes = graph[curr_city]["routes"]
    max_speed =0
    for route in routes:
        speed = route.get_speed()
        if( speed > max_speed ):
            max_speed = speed
    mpg = 2.6667*max_speed*math.pow((1- (max_speed/150)),4)
    return mpg
    
    
def compute_heuristic(ranges,curr_city,end_city,cost_function,graph):
    if cost_function == "distance" or cost_function == "segments":
        curr_city = graph[curr_city]["city"]
        end_city = graph[end_city]["city"]

        return abs(compute_distance(ranges,curr_city,end_city,graph))
    elif cost_function == "time":
        curr_city = graph[curr_city]["city"]
        end_city = graph[end_city]["city"]
        dist = compute_distance(ranges,curr_city,end_city,graph)
        return compute_time(curr_city.get_name(),dist,graph)
    elif cost_function == "mpg":
        return compute_mpg(curr_city,graph)
        
def successors(city_name,graph,path_dict):
    routes = graph[city_name]["routes"]
    return [ graph[route.get_to_name()]["city"] for route in routes if route.get_to_name() if route.get_to_name() not in path_dict.keys()]


    
def find_solution(ranges,start_city,end_city,cost_function,graph):
    fringe = PriorityQueue()
    path_dict ={}
    est_cost = compute_heuristic(ranges,start_city,end_city,cost_function,graph)
    cumm_cost = 0
    #city = graph[start_city]["city"]
    path_dict[start_city] = [start_city]
    fringe.put((est_cost+cumm_cost,(cumm_cost,start_city)))
    while not fringe.empty():
        (est_cost,(cost,city)) = fringe.get()
        for (succ) in successors(city,graph,path_dict):
            if succ.get_name() == end_city:
                path_dict[succ.get_name()] = path_dict[city] + [succ.get_name()]
                return path_dict[succ.get_name()]
            est_cost = compute_heuristic(ranges,succ.get_name(),end_city,cost_function,graph)
            if cost_function == "segments":
                fringe.put((est_cost + cost+1,(cost+1,succ.get_name())))
            elif cost_function == "distance":
                distance = 0
                for route in graph[city]["routes"]:
                    if route.get_to_name() == succ.get_name():
                        distance = route.get_distance()
                fringe.put((est_cost + distance ,(cost+ distance,succ.get_name())))
            elif cost_function == "time" :
                time = 0
                for route in graph[city]["routes"]:
                    if route.get_to_name() == succ.get_name():
                        distance = route.get_distance()
                        speed = route.get_speed()
                        time = distance/speed
                fringe.put((est_cost + time,(cost+ time,succ.get_name())))
            elif cost_function == "mpg":
                mpg = 0
                for route in graph[city]["routes"]:
                    if route.get_to_name() == succ.get_name():
                        speed = route.get_speed()
                        mpg  =  2.6667*speed*math.pow((1- (speed/150)),4)
                fringe.put(( -(abs(est_cost) + mpg),(cost+ mpg,succ.get_name()))) 
                        
            path_dict[succ.get_name()] = path_dict[city] + [succ.get_name()]

    return None

def preprocess_data(cities,routes):
     city_list = [city.get_name() for city in cities]
     for way in routes:
        city_state = way.get_from_name()
        if city_state not in city_list:
            _,state = city_state.split(",_") 
            missed_city = city(str(city_state),str(state),float(-1),float(-1))
            cities.append(missed_city)
            city_list.append(city_state)
     return cities,routes
 
    
def compute_ranges(graph):
    "Includes all the cities which were not initially present in city-gps.txt and were later added" 
    mega_count = 0 
    "Includes  cities which are  present only in city-gps.txt"
    count =0 
    lat = 0
    long =0
    ranges =[]
    for key,value in graph.items():
        city = value["city"]
        latitude = city.get_latitude()
        longitude = city.get_longitude()
        mega_count += 1
        if latitude != -1 and longitude != -1 :  
            count += 1
            lat  += latitude
            long += longitude
    lat_avg = ((lat/count) + (lat/mega_count))/2
    long_avg = ((long/count) + (long/mega_count))/2
    ranges.append(lat_avg)
    ranges.append(long_avg)
    return ranges
            
                            
if __name__ == "__main__":
    
    start_city = str(sys.argv[1]).replace('"',"")
    end_city =  str(sys.argv[2]).replace('"',"")
    cost_function =  str(sys.argv[3])
    cities = []
    routes= []
    with open("city-gps.txt", 'r') as file:
        for line in file:
            city_state,latitude,logitude = line.split()
            _,state = city_state.split(",_") 
            c = city(str(city_state).replace('"',""),str(state),float(latitude),float(logitude))
            cities.append(c)
    with open("road-segments.txt", 'r') as file:
        for line in file:
            from_city_state,to_city_state,length,speed,highway = line.split()
            r1 = route(str(from_city_state).replace('"',""),str(to_city_state).replace('"',""),int(length),int(speed),str(highway))
            r2 = route(str(to_city_state).replace('"',""),str(from_city_state).replace('"',""),int(length),int(speed),str(highway))
            routes.append(r1)
            routes.append(r2)
    cities,routes = preprocess_data(cities,routes)
    network = road_network(cities,routes)
    graph = network.build_netwrok()
    ranges = compute_ranges(graph)
    solution = find_solution(ranges,start_city,end_city,cost_function,graph)
    print(ranges)
    segments = 0
    distance = 0
    time =0
    fuel = 0
    start_city = solution[0]
    end_city = solution[len(solution) - 1]
    for i in range(0,len(solution)): 
        if(i +1 < len(solution)):
           start_city = solution[i]
           end_city = solution[i+1]
           for route in graph[start_city]["routes"]:
               if route.get_to_name() == end_city :
                   segments += 1
                   speed = route.get_speed()
                   distance += route.get_distance()
                   time += route.get_distance()/speed
                   mpg =  2.6667*speed*math.pow((1- (speed/150)),4)
                   fuel += route.get_distance()/mpg
                   
    print( str(segments) + " " + str(distance) + " " + str(round(float(time),4)) + " " + str(round(float(fuel),4)) + " " + " ".join(solution) )
                   
                   
               
        
       
            
  
                 
        
   

    
