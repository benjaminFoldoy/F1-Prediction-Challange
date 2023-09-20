import requests
import xmltodict
import os
from colorama import Fore, Back, Style

# Specify the API endpoint URL and any required parameters
def query_from_list(_list, subtract_from_text = ""):
    print("SELECT INDEX FROM LIST:\n")
    for i, entry in enumerate(_list):
        print(str(i) + ":  " + str(entry).replace(subtract_from_text, ""))
    while True:
        try:
            return _list[int(input("\n:  "))]
        except:
            continue

def query_url():
    
    year = Fore.GREEN + "*YEAR*" + Fore.WHITE
    round = Fore.GREEN + "*ROUND*" + Fore.WHITE
    driverid = Fore.GREEN + "*DRIVER ID*" + Fore.WHITE
    constructorid = Fore.GREEN + "*CONSTRUCTOR ID*" + Fore.WHITE
    circuitid = Fore.GREEN + "*CIRCUIT ID*" + Fore.WHITE
    lapnumber = Fore.GREEN + "*LAP NUMBER*" + Fore.WHITE
    pitstopnumber = Fore.GREEN + "*PIT STOP NUMBER*" + Fore.WHITE
    
    year = "*YEAR*"
    round = "*ROUND*"
    driverid = "*DRIVER ID*"
    constructorid = "*CONSTRUCTOR ID*"
    circuitid = "*CIRCUIT ID*" 
    lapnumber = "*LAP NUMBER*"
    pitstopnumber = "*PIT STOP NUMBER*"

    urls = [
        f"http://ergast.com/api/f1/{year}/drivers",
        f"http://ergast.com/api/f1/{year}/{round}/drivers",
        f"http://ergast.com/api/f1/drivers/{driverid}",
        f"http://ergast.com/api/f1/constructors",
        f"http://ergast.com/api/f1/{year}/constructors",
        f"http://ergast.com/api/f1/{year}/{round}/constructors",
        f"http://ergast.com/api/f1/constructors/{constructorid}",
        f"http://ergast.com/api/f1/circuits.json",
        f"http://ergast.com/api/f1/{year}/circuits",
        f"http://ergast.com/api/f1/{year}/circuits",
        f"http://ergast.com/api/f1/{year}/{round}/circuits",
        f"http://ergast.com/api/f1/circuits/{circuitid}",
        f"http://ergast.com/api/f1/seasons",
        f"http://ergast.com/api/f1/{year}/{round}/results",
        f"http://ergast.com/api/f1/current/last/results",
        f"http://ergast.com/api/f1/{year}/{round}/qualifying",
        f"http://ergast.com/api/f1/{year}",
        f"http://ergast.com/api/f1/current",
        f"http://ergast.com/api/f1/{year}/{round}",
        f"http://ergast.com/api/f1/{year}/{round}/driverStandings",
        f"http://ergast.com/api/f1/{year}/{round}/constructorStandings",
        f"http://ergast.com/api/f1/{year}/driverStandings",
        f"http://ergast.com/api/f1/{year}/constructorStandings",
        f"http://ergast.com/api/f1/current/driverStandings",
        f"http://ergast.com/api/f1/current/constructorStandings",
        f"http://ergast.com/api/f1/driverStandings/1",
        f"http://ergast.com/api/f1/constructorStandings/1",
        f"http://ergast.com/api/f1/drivers/{driverid}/driverStandings",
        f"http://ergast.com/api/f1/constructors/{constructorid}/constructorStandings",
        # f"http://ergast.com/api/f1/status",
        # f"http://ergast.com/api/f1/{year}/status",
        # f"http://ergast.com/api/f1/{year}/{round}/status",
        # f"http://ergast.com/api/f1/{year}/{round}/laps/{lapnumber}",
        # f"http://ergast.com/api/f1/{year}/{round}/pitstops",
        # f"http://ergast.com/api/f1/{year}/{round}/pitstops/{pitstopnumber}"
    ]
    return query_from_list(urls, subtract_from_text = "http://ergast.com/api/f1/")

def query_year():
    while True:
        year = input("Year:   ")
        try:
            return int(year)
        except:
            continue

def query_round():
    while True:
        round = input("Round:   ")
        try:
            return  int(round)
        except:
            continue


def query_driver_id():
    drivers = ["albon", "alonso", "de vries", "gasly", "hamilton", "hulkenberg", "leclerc", "magnussen", "norris", "ocon", "perez", "piastri", "russel", "sainz", "sargeant", "stroll", "tsunoda", "verstappen", "zhou"]
    return query_from_list(drivers)

def query_constructor_id():
    constructors = ["alfa", "alphatauri", "alpine", "aston_martin", "ferrari", "haas", "mclaren", "mercedes", "red_bull", "williams"]
    return(query_from_list(constructors))

def create_request_url():
    url = query_url()
    if url.count("*YEAR*") > 0:
        year = query_year()
        url = url.replace("*YEAR*", str(year))
    if url.count("*ROUND*") > 0:
        year = query_round()
        url = url.replace("*ROUND*", str(year))
    if url.count("*DRIVER ID*") > 0:
        year = query_driver_id()
        url = url.replace("*DRIVER ID*", str(year))
    if url.count("*CONSTRUCTOR ID*") > 0:
        year = query_constructor_id()
        url = url.replace("*CONSTRUCTOR ID*", str(year))
    if url.count("*CIRCUIT ID*") > 0:
        #l8r sk8r
        url = url.replace("*CIRCUIT ID*", str(year))
    if url.count("*LAP NUMBER*") > 0:
        #l8r sk8r
        url = url.replace("*LAP NUMBER*", str(year))
    if url.count("*PIT STOP NUMBER*") > 0:
        #l8r sk8r
        url = url.replace("*PIT STOP NUMBER*", str(year))
    
    print(url)
    return url


def Ask(url):
    response = requests.get(url)
    f1_dict = xmltodict.parse(response.text)

    path = []

    while True:
        print(url)
        print(Fore.WHITE)
        current_folder = f1_dict
        for f_name in path: #nesting into the dic
            current_folder = current_folder[f_name]
            if type(f_name) == int:
                print("["+ str(f_name), end="]")
            else:
                print("['"+ str(f_name), end="']")
        print("\n\n")
        
        indexes = []
        if type(current_folder) == str:
            print(current_folder)
        else:
            for n, key in enumerate(current_folder):
                indexes.append(key)
                print(Fore.YELLOW + f"{n} - ", key)
            
        command = input(Fore.MAGENTA+"\n\n**Press enter to go back**\npress *index* + enter to nagivate to folder.\n\n" + Fore.WHITE)
        if command != "":
            if type(indexes[int(command)]) == dict:
                path.append(int(command))
            else:
                path.append(indexes[int(command)])
        else:
            path.pop()

if __name__ == "__main__":
    url = create_request_url()
    Ask(url)