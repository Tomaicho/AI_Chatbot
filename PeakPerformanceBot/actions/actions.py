# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class calculateTrailClimb(Action):

    def name(self) -> Text:
        return "calculate_trail_climb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        distance = next(tracker.get_latest_entity_values("goaldistance"), None)
        uphill = tracker.get_slot("ascent")
        downhill = tracker.get_slot("descent")
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
