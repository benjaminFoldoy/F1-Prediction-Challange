import requests
import xmltodict
import os
from colorama import Fore, Back, Style

def driver_standings():
    standings = []
    url = "http://ergast.com/api/f1/current/driverStandings"
    params = {"limit": 1000}
    response = requests.get(url, params=params)
    print(response.text)
    f1_dict = xmltodict.parse(response.text)
    
    for standing in f1_dict['MRData']['StandingsTable']['StandingsList']['DriverStanding']:
        standings.append(standing["Driver"]["GivenName"] + " " + standing["Driver"]["FamilyName"])
    
    return standings

def driver_standings_points(values_input):
    from write_to_google_sheet import get_cell_crd, get_cell_value, insert_into_cell
    closeness_points_dict = {0:10, 1:5, 2:3, 3:1}
    points = {"K":0, "B":0}
    
    standings_lists = {"K":[], "B":[]}
    
    for i in range(20):
        b_crd = get_cell_crd("K"+str(5+i))
        b_value = get_cell_value(b_crd, values_input)
        standings_lists["B"].append(b_value)
        
        k_crd = get_cell_crd("L"+str(5+i))
        k_value = get_cell_value(k_crd, values_input)
        standings_lists["K"].append(k_value)
    
    print(standings_lists)
    for i, driver in enumerate(driver_standings()):
        for key in standings_lists:
            guess_index = standings_lists[key].index(driver)
            diff = abs(guess_index - i) 
            if diff <= 3:
                points[key] += closeness_points_dict[diff]
            
    
    insert_into_cell("P27", points["B"], values_input)
    insert_into_cell("Q27", points["K"], values_input)
    return values_input