import requests
import json
from itertools import permutations

#ENTER YOUR API KEY into API_KEY
API_KEY = ""
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"


class City:
    def __init__(self, name, temperatures):
        self.name = name
        self.temps = temperatures

    def get_temperature(self, day):
        return self.temps[day]

    def __str__(self):
        return self.name


class Route:

    def __init__(self, citiesonroute):
        self.cities = citiesonroute



    def avgcost(self):
        temptemp = 0
        for j in range(len(self)):
            city = cities[j]
            temptemp += city.get_temperature(j)
        temptemp /= len(cities)
        return temptemp


    def __str__(self):
        return self.cities


def fetch_weather(id):
    # request parameter(s): Start with '?'
    # separate name and value with '='
    # multiple parameter name value pairs are separate with '&'
    query_string = "?id={}&units=imperial&APIKEY={}".format(id, API_KEY)
    request_url = WS_URL + query_string
    #print("Request URL: ", request_url)
    response = requests.get(request_url)
    if response.status_code == 200:
        d = response.json()
        city_name = d["city"]['name']
        lst = d['list']
        assert 40 == len(lst)
        tmp_list = []
        for i in range(len(lst) // 8):
            li = [x for x in range(len(lst)) if x // 8 == i]
            tmp_list.append(max([lst[j]["main"]["temp_max"] for j in li]))
        return City(city_name, tmp_list)
    else:
        print("How should I know?")
        return None


if __name__ == "__main__":
    id_list = json.loads(open("cities.json").read())
    cities = []
    for id in id_list:
        cities.append(fetch_weather(id))
    avg_temp = 0
    for i in range(len(cities)):
        city = cities[i]
        print(city)
        avg_temp += city.get_temperature(i)
    avg_temp /= len(cities)
    print(avg_temp)
    p = list(permutations(cities))
    lowest_temp = Route.avgcost(p[0])
    previouscost = Route.avgcost(p[0])
    for i in range(len(p)):
    #for iter in p:
        Route(p[i])
        if Route.avgcost(p[i]) < previouscost and Route.avgcost(p[i]) < lowest_temp:
            lowest_temp = Route.avgcost(p[i])
        '''FOR SOME REASON THE ITERATION IS NOT CHANGING IN "ROUTE.CITIES" AND IT WON'T CHANGE THE CITIES FOR SOME REASON.'''
        previouscost = Route.avgcost(p[i])
    print(lowest_temp)