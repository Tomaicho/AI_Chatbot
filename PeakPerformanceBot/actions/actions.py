# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re


class calculateTrailClimb(Action):

    def name(self) -> Text:
        return "calculate_trail_climb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        distance = next(tracker.get_latest_entity_values("goaldistance"), None)
        uphill = tracker.get_slot("ascent")
        # downhill = tracker.get_slot("descent")
        distance_unit = next(tracker.get_latest_entity_values("goaldistanceunit"), None)

        if not uphill:
            msg = "To define the best training plan I need to know the total uphill climb of the race."
            dispatcher.utter_message(text=msg)
            return []


        if distance_unit == "m":
            distance = int(distance)
        else:
            distance = int(distance)*1000

        uphill = int(uphill)

        ratio = uphill/distance
        if ratio > 0.055:
            dispatcher.utter_message(response = "utter_big_climb")
        else:
            dispatcher.utter_message(response = "utter_small_climb")
        return []

# class ValidateRaceInfoForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_race_info_form"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         goal_hours = tracker.get_slot("goalhours")
#         goal_minutes = tracker.get_slot("goalminutes")
#         goal_seconds = tracker.get_slot("goalseconds") 

        
#     def validate_goaltime(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:   
        
        
        
#         return {"goalhours":slot_value}
    

class convertTime(Action):
    def name(self) -> Text:
        return "convert_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        goal_hours = tracker.get_slot("goalhours")
        goal_minutes = tracker.get_slot("goalminutes")
        goal_seconds = tracker.get_slot("goalseconds")

        if goal_hours != None:
            match = re.search(r'[0-9]+', goal_hours)
            if match:
                hours = int(match.group())
        else:
            hours = 0
        if goal_minutes != None:
            match = re.search(r'[0-9]+', goal_minutes)
            if match:
                minutes = int(match.group())
        else:
            minutes = 0
        if goal_seconds != None:
            match = re.search(r'[0-9]+', goal_seconds)
            if match:
                seconds = int(match.group())
        else:
            seconds = 0
        
        finalseconds = (hours*3600) + (minutes*60) + seconds
        return[SlotSet("goaltimefinal", finalseconds)]

class convertDistance(Action):
    def name(self) -> Text:
        return "convert_distance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        goaldistance_km = tracker.get_slot("goaldistance_km")
        goaldistance_m = tracker.get_slot("goaldistance_m")
        

        if goaldistance_km != None:
            match = re.search(r'[0-9]+', goaldistance_km)
            if match:
                km = int(match.group())
        else:
            km = 0
        if goaldistance_m != None:
            match = re.search(r'[0-9]+', goaldistance_m)
            if match:
                m = int(match.group())
        else:
            m = 0
        
        finalmetres = (km*1000) + m 
        return[SlotSet("goaldistancefinal", finalmetres)]

class convertTimeLeft(Action):
    def name(self) -> Text:
        return "convert_time_left"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        tl_days = tracker.get_slot("time_left_days")
        tl_years = tracker.get_slot("time_left_years")
        tl_months = tracker.get_slot("time_left_months")
        tl_weeks = tracker.get_slot("time_left_weeks")

        if tl_days != None:
            match = re.search(r'[0-9]+', tl_days)
            if match:
                days = int(match.group())
        else:
            days = 0
        if tl_months != None:
            match = re.search(r'[0-9]+', tl_months)
            if match:
                months = int(match.group())
        else:
            months = 0
        if tl_years != None:
            match = re.search(r'[0-9]+', tl_years)
            if match:
                years = int(match.group())
        else:
            years = 0
        if tl_weeks != None:
            match = re.search(r'[0-9]+', tl_weeks)
            if match:
                weeks = int(match.group())
        else:
            weeks = 0
        
        finaldays = (years*365) + (months*30) + (weeks*7) + days
        finalweeks = finaldays//7
        return[SlotSet("time_left_final", finalweeks)]