# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

from fuzzywuzzy import process
import math


#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

def get_most_matched_string(query, choices, limit=4):
    results = process.extract(query, choices, limit=limit)
    return results


def getIndiaStatesList():
    url = "https://api.covid19india.org/data.json"
    data = ((requests.get(url)).json())
    states = []
    for key in data['statewise']:
        states.append(key['state'])

    states.remove('Total')
    states.remove('State Unassigned')

    return states


def getIndiaDistrictList():
    url = "https://api.covid19india.org/state_district_wise.json"

    data = ((requests.get(url)).json())
    states = []
    districts = []
    district_state_dictionary = {}

    for key in data.items():
        states.append(key[0])

    for state in states:
        for key in (data[state]['districtData']).items():
            district = key[0]
            district_state_dictionary[district] = state
            districts.append(district)
    return districts, district_state_dictionary


def getCovidStats(state, district):
    url = "https://api.covid19india.org/state_district_wise.json"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    covid_stats = data[state]['districtData'][district]

    cases_in_the_last_24_hours = covid_stats['delta']['confirmed']
    deaths_in_the_last_24_hours = covid_stats['delta']['deceased']
    recoveries_in_the_last_24_hours = covid_stats['delta']['recovered']

    total_cases_reported = covid_stats['confirmed']
    total_deaths = covid_stats['deceased']
    total_active_cases = covid_stats['active']

    covid_stats_pretty_print = f"""🤍
    COVID-19 stats of '{district}, {state}':
    ----------------------------------------
    Cases in the last 24 hours: {cases_in_the_last_24_hours}
    Deaths in the last 24 hours: {deaths_in_the_last_24_hours}
    Recoveries in the last 24 hours: {recoveries_in_the_last_24_hours}
    -----------------------------------------
    Total cases reported: {total_cases_reported}
    Total deaths: {total_deaths}
    Total active cases: {total_active_cases}
    -----------------------------------------
    """
    return covid_stats_pretty_print


class API:

    def getPostOfficeDetails(pincode):

        url = f"https://api.postalpincode.in/pincode/{pincode}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        # extract data in json format
        data = response.json()

        state_name = data[0]['PostOffice'][0]['State']
        district_name = data[0]['PostOffice'][0]['District']

        result = [state_name, district_name]

        return result

    def getCovidStatsOfIndia():
        url = "https://api.covid19india.org/data.json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()

        covid_stats = data['statewise'][0]

        cases_in_the_last_24_hours = covid_stats['deltaconfirmed']
        deaths_in_the_last_24_hours = covid_stats['deltadeaths']
        recoveries_in_the_last_24_hours = covid_stats['deltarecovered']

        total_cases_reported = covid_stats['confirmed']
        total_deaths = covid_stats['deaths']
        total_active = covid_stats['active']

        covid_stats_pretty_print = f"""🤍
        COVID-19 stats of India:
        ----------------------------------------
        Cases in the last 24 hours: {cases_in_the_last_24_hours}
        Deaths in the last 24 hours: {deaths_in_the_last_24_hours}
        Recoveries in the last 24 hours: {recoveries_in_the_last_24_hours}
        -----------------------------------------
        Total cases reported: {total_cases_reported}
        Total deaths: {total_deaths}
        Total active cases: {total_active}
        -----------------------------------------
        """
        return covid_stats_pretty_print

    def getCovidStatsOfCity(city):

        url = "https://api.covid19india.org/data.json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()

        all_states_data = data['statewise']

        states = getIndiaStatesList()
        districts, district_state_pair = getIndiaDistrictList()

        cities = states + districts
        # this will contain most matched states list; can be used if decided to show suggestion to user
        matched_city = get_most_matched_string(city, cities)
        print(matched_city)

        if matched_city[0][0] in states:
            current_state = matched_city[0][0]
            index = 0
            for state_specific_data in all_states_data:
                if state_specific_data['state'] == current_state:
                    break
                index += 1

            covid_stats = data['statewise'][index]
            cases_in_the_last_24_hours = covid_stats['deltaconfirmed']
            deaths_in_the_last_24_hours = covid_stats['deltadeaths']
            recoveries_in_the_last_24_hours = covid_stats['deltarecovered']

            total_cases_reported = covid_stats['confirmed']
            total_deaths = covid_stats['deaths']
            total_active = covid_stats['active']

            covid_stats_pretty_print = f"""🤍
            COVID-19 stats of {current_state}:
            ----------------------------------------
            Cases in the last 24 hours: {cases_in_the_last_24_hours}
            Deaths in the last 24 hours: {deaths_in_the_last_24_hours}
            Recoveries in the last 24 hours: {recoveries_in_the_last_24_hours}
            -----------------------------------------
            Total cases reported: {total_cases_reported}
            Total deaths: {total_deaths}
            Total active cases: {total_active}
            -----------------------------------------
            """
            return covid_stats_pretty_print
        else:
            state = district_state_pair[matched_city[0][0]]
            return getCovidStats(state, matched_city[0][0])


class ActionGetCovidStats(Action):

    def name(self) -> Text:
        return "action_get_covid_stats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode_slot_value = tracker.get_slot("pincode")

        details_from_pincode = API.getPostOfficeDetails(pincode_slot_value)
        state_name = details_from_pincode[0]
        district_name = details_from_pincode[1]

        url = "https://api.covid19india.org/data.json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()

        all_states_data = data['statewise']

        states = getIndiaStatesList()
        districts, district_state_pair = getIndiaDistrictList()

        cities = states + districts

        matched_districtname = get_most_matched_string(district_name, cities)
        matched_statename = get_most_matched_string(state_name, cities)

        covid_stats_pretty_print = getCovidStats(
            matched_statename[0][0], matched_districtname[0][0])

        dispatcher.utter_message(text=covid_stats_pretty_print)
        return []


class ActionCheckStoredPincodeAskUserBack(Action):

    def name(self) -> Text:
        return "action_check_stored_pincode_ask_user_back"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode_slot_value = tracker.get_slot("pincode")
        print(" "+pincode_slot_value)

        if pincode_slot_value == '':
            dispatcher.utter_message(
                text="Please provide a pincode or district name that you want to search for")
        else:
            details_from_pincode = API.getPostOfficeDetails(pincode_slot_value)
            state_name = details_from_pincode[0]
            district_name = details_from_pincode[1]

            ask_user = f"""Do you want to know about cases in {district_name}({pincode_slot_value})?"""

            dispatcher.utter_message(text=ask_user)

        return []


class ActionFetchStatsForStoredPincode(Action):

    def name(self) -> Text:
        return "action_fetch_stats_for_stored_pincode"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode_slot_value = tracker.get_slot("pincode")
        details_from_pincode = API.getPostOfficeDetails(pincode_slot_value)
        state_name = details_from_pincode[0]
        district_name = details_from_pincode[1]

        url = "https://api.covid19india.org/data.json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()

        all_states_data = data['statewise']

        states = getIndiaStatesList()
        districts, district_state_pair = getIndiaDistrictList()

        cities = states + districts

        matched_districtname = get_most_matched_string(district_name, cities)
        matched_statename = get_most_matched_string(state_name, cities)

        covid_stats_pretty_print = getCovidStats(
            matched_statename[0][0], matched_districtname[0][0])

        dispatcher.utter_message(text=covid_stats_pretty_print)

        return []


class ActionFetchCovidStatsForCity(Action):

    def name(self) -> Text:
        return "action_fetch_covid_stats_for_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cityname_slot_value = tracker.get_slot("cityname")
        print(cityname_slot_value)
        covid_stats_pretty_print = API.getCovidStatsOfCity(
            cityname_slot_value)

        dispatcher.utter_message(text=covid_stats_pretty_print)

        return []


class ActionFetchCovidStatsForIndia(Action):

    def name(self) -> Text:
        return "action_fetch_covid_stats_for_india"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        covid_stats_of_india = API.getCovidStatsOfIndia()

        dispatcher.utter_message(text=covid_stats_of_india)

        return []


class ActionAskUsername(Action):

    def name(self) -> Text:
        return "action_ask_username"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username_slot_value = tracker.get_slot("username")

        if username_slot_value == None:
            dispatcher.utter_message(text="What is your name?")
        else:
            greet_user = f"""Hello {username_slot_value}, How can I help you?"""
            dispatcher.utter_message(text=greet_user)

        return []


class ActionFetchResultsForPincodeInWords(Action):

    def name(self) -> Text:
        return "action_fetch_results_for_pincode_in_words"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity_value = tracker.latest_message['entities'][0]['value']
        entity_text = tracker.latest_message['entities'][0]['text']

        pincode = 0
        if len(tracker.latest_message['entities']) == 6:
            for entity_info in tracker.latest_message['entities']:
                pincode = pincode*10 + entity_info['value']
        else:
            dispatcher.utter_message(
                text="Please enter 6 digit valid pincode either in numbers only or each digit spelled in words separated by space")
            return []

        details_from_pincode = API.getPostOfficeDetails(pincode)
        state_name = details_from_pincode[0]
        district_name = details_from_pincode[1]

        covid_stats_pretty_print = getCovidStats(state_name, district_name)

        dispatcher.utter_message(text=covid_stats_pretty_print)

        return []
