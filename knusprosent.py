import requests
import xmltodict
import datetime
from colorama import Fore, Back, Style

driver_pairs = {
    "B":[
        ["leclerc", "sainz"],
        ["max_verstappen", "perez"],
        ["tsunoda", "de_vries"],
        ["hamilton", "russell"],
        ["ocon", "gasly"],
        ["albon", "sargeant"],
        ["alonso", "stroll"],
        ["kevin_magnussen", "hulkenberg"],
        ["bottas", "zhou"],
        ["norris", "piastri"]
    ],
    "K":[
        ["leclerc", "sainz"],
        ["max_verstappen", "perez"],
        ["de_vries", "tsunoda"],
        ["hamilton", "russell"],
        ["gasly", "ocon"],
        ["albon", "sargeant"],
        ["alonso", "stroll"],
        ["kevin_magnussen", "hulkenberg"],
        ["bottas", "zhou"],
        ["norris", "piastri"]
    ],
}

def get_finished_races_count():
    count = 0
    url = "http://ergast.com/api/f1/current"
    response = requests.get(url)
    f1_dict = xmltodict.parse(response.text)
    for race in f1_dict['MRData']['RaceTable']['Race']:
        if datetime.datetime.fromisoformat(race["Date"]) < datetime.datetime.now():
            count += 1
    return count

def get_driver_position(driver_id, round):
    url = f"http://ergast.com/api/f1/2023/{round}/results"
    response = requests.get(url)
    f1_dict = xmltodict.parse(response.text)
    
    for driver in f1_dict['MRData']['RaceTable']['Race']['ResultsList']['Result']:
        if driver['Driver']['@driverId'] == driver_id:
            return driver['@position']

def get_driver_name(driver_id):
    url = f"http://ergast.com/api/f1/drivers/{driver_id}"
    response = requests.get(url)
    f1_dict = xmltodict.parse(response.text)
    
    return f1_dict['MRData']['DriverTable']['Driver']['GivenName'] + " " + f1_dict['MRData']['DriverTable']['Driver']['FamilyName']

def get_round_dvd_winner(driver_id1, driver_id2, round):
    if get_driver_position(driver_id1, round) < get_driver_position(driver_id2, round):
        return driver_id1
    return driver_id2

def get_season_dvd_winner(driver_id1, driver_id2):
    count_driver_1 = 0
    count_driver_2 = 0
    fr_count = get_finished_races_count()
    for n in range(fr_count):
        if get_round_dvd_winner(driver_id1, driver_id2, n+1) == driver_id1:
            count_driver_1 += 1
        else: count_driver_2 += 1
    if count_driver_1 >= count_driver_2:
        return driver_id1
    return driver_id2

def get_knusprosent(driver_id1, driver_id2):
    races_count = get_finished_races_count()
    driver_1_count = 0
    for n in range(1, races_count+1):
        if get_driver_position(driver_id1, n) < get_driver_position(driver_id2, n):
            driver_1_count += 1
    return driver_1_count/races_count

def update_values_sheet(values_input):
    from write_to_google_sheet import get_cell_crd, get_cell_value, insert_into_cell
    guess_crds = {"B":"G37", "K":"J37"}
    
    diffs = {"B":[], "K":[]}
    print(Fore.CYAN + f"PROGRESS: 0.0%" + Fore.WHITE)
    progress = 0
    for key in driver_pairs:
        for i, pairing in enumerate(driver_pairs[key]):
            actual_winner_id = get_season_dvd_winner(pairing[0], pairing[1])
            actual_winner_name = get_driver_name(actual_winner_id) #from winner id to name
            
            d2 = pairing[0]
            if actual_winner_id == d2:
                d2 = pairing[1]
            
            g_crd = get_cell_crd(guess_crds[key])
            
            knusprosent = get_knusprosent(actual_winner_id, d2)
            
            insert_into_cell("M"+str(37+i), knusprosent, values_input)
            
            guess = float(get_cell_value([g_crd[0], g_crd[1]+i]).replace("%", ""))*0.01
            
            diffs[key].append(abs(guess - knusprosent))
            progress += 1
            print(Fore.CYAN + f"PROGRESS: {(progress/(len(driver_pairs)*len(driver_pairs['B'])))*100}%" + Fore.WHITE)
    points = {"B":0, "K":0}
    for i in range(len(diffs["B"])):
        if diffs["B"][i] < diffs["K"][i]:
            points["B"] += 5
            
        elif diffs["B"][i] != diffs["K"][i]:
            points["K"] += 5
    
    insert_into_cell("P29", points["B"], values_input)
    insert_into_cell("Q29", points["K"], values_input)

if __name__ == "__main__":
    p=update_values_sheet()
    print(p)