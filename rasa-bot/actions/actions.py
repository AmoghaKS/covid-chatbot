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


class ActionGetCovidStats(Action):

    def name(self) -> Text:
        return "action_get_covid_stats"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        pincode_slot_value = tracker.get_slot("pincode")
        result = API.getPostOfficeDetails(pincode_slot_value)

        state_name = result[0]
        district_name = result[1]

        url = "https://api.covid19india.org/state_district_wise.json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()
        covid_stats = data[state_name]['districtData'][district_name]

        # print(covid_stats)
        cases_in_the_last_24_hours = covid_stats['delta']['confirmed']
        deaths_in_the_last_24_hours = covid_stats['delta']['deceased']
        recoveries_in_the_last_24_hours = covid_stats['delta']['recovered']

        total_cases_reported = covid_stats['confirmed']
        total_deaths = covid_stats['deceased']
        total_active_cases = covid_stats['active']

        covid_stats_pretty_print = f"""
        
        COVID19 stats in '{district_name}':
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
        # print(covid_stats_pretty_print)
        # # print(response.text)

        dispatcher.utter_message(text=covid_stats_pretty_print)
        return []
