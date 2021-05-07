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

        covid_stats_pretty_print = f""".
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

    def getCovidStatsOfIndia():
        url = "https://api.covid19india.org/data.json"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        data = response.json()

        covid_stats = data['cases_time_series'][-1]

        cases_in_the_last_24_hours = covid_stats['dailyconfirmed']
        deaths_in_the_last_24_hours = covid_stats['dailydeceased']
        recoveries_in_the_last_24_hours = covid_stats['dailyrecovered']

        total_cases_reported = covid_stats['totalconfirmed']
        total_deaths = covid_stats['totaldeceased']
        total_recovered = covid_stats['totalrecovered']

        covid_stats_pretty_print = f""".
        COVID-19 stats of India:
        ----------------------------------------
        Cases in the last 24 hours: {cases_in_the_last_24_hours}
        Deaths in the last 24 hours: {deaths_in_the_last_24_hours}
        Recoveries in the last 24 hours: {recoveries_in_the_last_24_hours}
        -----------------------------------------
        Total cases reported: {total_cases_reported}
        Total deaths: {total_deaths}
        Total recoveries: {total_recovered}
        -----------------------------------------
        """
        return covid_stats_pretty_print


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

        covid_stats_pretty_print = API.getCovidStats(state_name, district_name)

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

        covid_stats_pretty_print = API.getCovidStats(state_name, district_name)

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
