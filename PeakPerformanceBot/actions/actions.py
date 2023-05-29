# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
import random
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
import re


class calculateTrailClimb(Action):

    def name(self) -> Text:
        return "calculate_trail_climb"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        distance = tracker.get_slot("goaldistancefinal")
        uphill = tracker.get_slot("ascent_number")
        # downhill = tracker.get_slot("descent")

        if not uphill:
            # msg = "To define the best training plan I need to know the total uphill climb of the race."
            # dispatcher.utter_message(text=msg)
            # return [FollowupAction(name='action_listen')]
            return [SlotSet("climb_ratio", "small")]
        else:
            uphill = int(uphill)

        distance = int(distance)
        ratio_up = uphill/distance
        if ratio_up > 0.055:
            return [SlotSet("climb_ratio", "big")]
        else:
            return [SlotSet("climb_ratio", "small")]
        

class calculateTrailDescent(Action):

    def name(self) -> Text:
        return "calculate_trail_descent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        distance = tracker.get_slot("goaldistancefinal")
        downhill = tracker.get_slot("descent_number")

        if not downhill:
            # msg = "To define the best training plan I need to know the total downhill of the race."
            # dispatcher.utter_message(text=msg)
            # return [FollowupAction(name='action_listen')]
            return [SlotSet("descent_ratio", "small")]
        else:
            downhill = int(downhill)

        distance = int(distance)
        ratio_down = downhill/distance
        if ratio_down > 0.055:
            return [SlotSet("descent_ratio", "big")]
        else:
            return [SlotSet("descent_ratio", "small")]
        

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
        return[SlotSet("time_leftfinal", finalweeks)]

class convertAscent(Action):
    def name(self) -> Text:
        return "convert_ascent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        ascent = tracker.get_slot("ascent")

        if ascent != None:
            match = re.search(r'[0-9]+', ascent)
            if match:
                ascent_number = int(match.group())
        else:
            ascent_number = 0
        
        return[SlotSet("ascent_number", ascent_number)]

class convertDescent(Action):
    def name(self) -> Text:
        return "convert_descent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        descent = tracker.get_slot("descent")

        if descent != None:
            match = re.search(r'[0-9]+', descent)
            if match:
                descent_number = int(match.group())
        else:
            descent_number = 0
        
        return[SlotSet("descent_number", descent_number)]
    

class recreationalRunner(Action):

    def name(self) -> Text:
        return "recreational_runner"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return[SlotSet("goaltimefinal", 9999999999999999)]
    

class defineTraining(Action):

    def name(self) -> Text:
        return "action_define_training"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Please wait while your training is being prepared.")

        distance = int(tracker.get_slot("goaldistancefinal"))
        racetype = tracker.get_slot("racetype")
        time_left = int(tracker.get_slot("time_leftfinal"))
        goal_time = tracker.get_slot("goaltimefinal")
        fitness = int(tracker.get_slot("current_fitness"))

        if not goal_time:
            goal_time = 99999999999
        else:
            goal_time = int(goal_time)

        with open("./download_train/db.json", encoding="utf-8") as file:
            db = json.load(file)
        
        if racetype == "trail":
            descent = tracker.get_slot("descent_ratio")
            ascent = tracker.get_slot("climb_ratio")
            up_meters = tracker.get_slot("ascent_number")
            down_meters = tracker.get_slot("descent_number")
            goal_time = goal_time / 60
            distance = distance / 1000
            pace = goal_time / distance
            pace = pace - up_meters / 500
            pace = pace + down_meters / 2000

            if pace < 5.5:
                difficult = True
            else:
                difficult = False

            extra_weeks = time_left % 4

            blocks = time_left // 4
            if time_left <= 5:  
                training_plan = self.weekPlansLittleTime(extra_weeks, fitness, time_left, db)
            else:
                training_plan = self.weekPlansTime(difficult, extra_weeks, blocks, fitness, time_left, db)
            
            if ascent == "big":
                msg = "\nSince the competition has a lot of climb, you must include at least two sessions per week.\n"
                training_plan += msg
                msg = "Focus on strengthening exercises for the legs and back, always finishing the sessions with some stretching and core."
                training_plan += msg
            if descent == "big":
                msg = "\nSince the competition has a lot of downhill, you must include some balance and running technique exercises along the week.\n"
                training_plan += msg
                msg = "It's good practice to do this kind of exercises before the tougher running sessions."
                training_plan += msg

        else:
            goal_time = goal_time / 60
            distance = distance / 1000
            pace = goal_time / distance

            if pace < 3.5 and distance > 20000:
                difficult = True
            elif pace < 3 and distance < 3000:
                difficult = True
            else:
                difficult = False

            extra_weeks = time_left % 4

            blocks = time_left // 4
            if time_left <= 5:  
                training_plan = self.weekPlansLittleTime(extra_weeks, fitness, time_left, db)
            else:
                training_plan = self.weekPlansTime(difficult, extra_weeks, blocks, fitness, time_left, db)
            

        return[SlotSet("training_plan", training_plan)]
    

    def weekPlansLittleTime(extra_weeks, fitness, time_left, db):
        training_plan = "\nSince there's not much time left, focus on maintaining a stable shape, without pushing too hard.\n"
        if extra_weeks == 0:
            for week in range(time_left - 1):
                msg = f"\nWeek {week+1}:\n"
                chance = random.randint(1,10)
                if chance <= fitness:
                    msg += "Moderate\n"
                    msg+= str(random.choice(db.get('moderate')))
                else:
                    msg += "Easy\n"
                    msg+= str(random.choice(db.get('easy')))
                training_plan += msg       
            msg = '\nFinish off with an easier tapering week to avoid arriving to the competition exhausted:\n'
            msg+= random.choice(db.get('easy'))
            training_plan += msg
            return(training_plan)
        else:
            for week in range(time_left - extra_weeks):
                chance = random.randint(1,10)
                msg = f"\nWeek {week+1}:\n"
                if chance <= fitness:
                    msg += "Moderate\n"
                    msg+= str(random.choice(db.get('moderate')))
                else:
                    msg += "Easy\n"
                    msg += str(random.choice(db.get('easy')))
                training_plan += msg   
            msg = '\nFinish off with an easier tapering period to avoid arriving to the competition exhausted:\n'
            training_plan+= msg  
            for week in range(extra_weeks):
                msg = str(random.choice(db.get('easy')))
                msg += '\n'
                training_plan += msg
            return(training_plan)
        
    def weekPlansTime(self, difficult, extra_weeks, blocks, fitness, time_left, db):
        training_plan = f"\nWe still have some time to prepare and achieve some good stuff. You'll receive a block of 4 training weeks, which you must repeat every 4 weeks. In total, you'll repeat this block {blocks} times.\n"
        if extra_weeks == 0:
            for week in range(4):
                msg = self.fetchWeeks(difficult, week, fitness, db) 
                training_plan += msg
            msg = '\nFinish off with an easier tapering week to avoid arriving to the competition exhausted:\n'
            msg+=random.choice(db.get('easy'))
            training_plan+=msg
            return(training_plan)
        else:
            for week in range(4):
                msg = self.fetchWeeks(difficult, week, fitness, db)
                training_plan+=msg  
            msg = '\nFinish off with an easier tapering period to avoid arriving to the competition exhausted:\n'
            training_plan+=msg  
            for week in range(extra_weeks):
                if extra_weeks - week > 2: 
                    msg = "Moderate\n"
                    msg += str(random.choice(db.get('moderate')))
                    msg += '\n'
                    training_plan += msg
                else:
                    msg = "Easy\n"
                    msg += str(random.choice(db.get('easy')))
                    msg += '\n'
                    training_plan += msg
                
            return(training_plan)
        
    def fetchWeeks(self, difficult, week, fitness, db):
        block_training = ''
        if difficult:
            msg = f"\nWeek {week+1}:\n"
            chance = random.randint(1,10)
            hard_chance = random.randint(3,7)
            # 3-> bad fitness doesn't train hard. 7-> Higher chance for good fitness to train hard because of difficult goal
            if chance <= fitness and hard_chance <= fitness:
                msg += "Hard\n"
                msg += str(random.choice(db.get('hard')))
            elif chance <= fitness and hard_chance > fitness:
                msg += "Moderate\n"
                msg += str(random.choice(db.get('moderate')))
            else:
                msg += "Easy\n"
                msg+=str(random.choice(db.get('easy')))
            block_training += msg 
        else:
            chance = random.randint(1,10)
            hard_chance = random.randint(3,10)
            # 3-> bad fitness doesn't train hard
            msg = f"\nWeek {week+1}:\n"
            if chance <= fitness and hard_chance <= fitness:
                msg += "Hard\n"
                msg+=str(random.choice(db.get('hard')))
            elif chance <= fitness and hard_chance > fitness:
                msg += "Moderate\n"
                msg+=str(random.choice(db.get('moderate')))
            else:
                msg += "Easy\n"
                msg+=str(random.choice(db.get('easy')))
            block_training += msg
        return(block_training)

class CheckSlotsFilledAction(Action):
    def name(self) -> Text:
        return "action_check_slots_filled"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        descent = tracker.get_slot("descent_ratio")
        ascent = tracker.get_slot("climb_ratio")
        distance = int(tracker.get_slot("goaldistancefinal"))
        racetype = tracker.get_slot("racetype")
        time_left = int(tracker.get_slot("time_leftfinal"))
        goal_time = int(tracker.get_slot("goaltimefinal"))
        fitness = int(tracker.get_slot("current_fitness"))

        if distance == None:
            dispatcher.utter_message(response = "utter_ask_goaldistancefinal")
            return[SlotSet("ready", False)]
        if time_left == None:
            dispatcher.utter_message(response = "utter_ask_time_leftfinal")
            return[SlotSet("ready", False)]
        if goal_time == None:
            dispatcher.utter_message(response = "utter_ask_goaltimefinal")
            return[SlotSet("ready", False)]
        if fitness == None:
            dispatcher.utter_message(response = "utter_ask_current_fitness")
            return[SlotSet("ready", False)]
        if racetype == None:
            dispatcher.utter_message(response = "utter_ask_racetype")
            return[SlotSet("ready", False)]
        
        else:
            if racetype == "trail":
                if descent == None:
                    dispatcher.utter_message(response = "utter_ask_descent")
                    return[SlotSet("ready", False)]
                if ascent == None:
                    dispatcher.utter_message(response = "utter_ask_ascent")
                    return[SlotSet("ready", False)]

        return [SlotSet("ready", True)]