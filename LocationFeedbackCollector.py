

from List import *
import time

class LocationFeedbackCollector:

    def __init__(self, location_name, feedback_list): # added list as argument
        self._name = location_name
        self._list = feedback_list  # Use the passed list instance

    #adds recent survey score to list array
    def recordFeedback(self, value): # Now takes a value
        self._list.append(value)