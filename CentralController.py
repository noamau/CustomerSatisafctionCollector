"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.
"""

# Import whatever Library classes you need - StateModel is obviously needed
# Counters imported for Timer functionality, Button imported for button events
from time import *
from random import *
from Log import *
from StateModel import *
from Counters import *
from Button import *
from Lights import *
from LightStrip import *
from Buzzer import *
from Displays import *
from LocationFeedbackCollector import *
from List import *

WomensWC = "Womens Restroom"
MensWC = "Mens Restroom"



"""
This is the template for a Controller - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the state model, you will need to implement __init__ and 4 other methods
to support model start, stop, entry actions, exit actions, and state actions.

The following methods must be implemented:
__init__: create instances of your View and Business model classes, create an instance
of the StateModel with the necessary number of states and add the transitions, buttons
and timers that the StateModel needs

stateEntered(self, state, event) - Entry actions
stateLeft(self, state, event) - Exit actions
stateDo(self, state) - do Activities

# A couple other methods are available - but they can be left alone for most purposes

run(self) - runs the State Model - this will start at State 0 and drive the state model
stop(self) - stops the State Model - will stop processing events and stop the timers

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class CentralController:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        
        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = StateModel(7, self, debug=True)
        
        # Instantiate any Buttons that you want to process events from and add
        # them to the model
        self._unsatisfied_button = Button(9, "button1", handler=None)
        self._neutral_button = Button(10, "button2", handler=None)    
        self._satisfied_button = Button(11, "button3", handler=None)    
        self._unsatisfied_button2 = Button(13, "button4", handler=None)    
        self._neutral_button2 = Button(14, "button5", handler=None)    
        self._satisfied_button2 = Button(15, "button6", handler=None)    
        self._reset_button = Button(28, "button7", handler=None) 

        self._model.addButton(self._unsatisfied_button)
        self._model.addButton(self._neutral_button)
        self._model.addButton(self._satisfied_button)

        self._model.addButton(self._unsatisfied_button2)
        self._model.addButton(self._neutral_button2)
        self._model.addButton(self._satisfied_button2)
        
        self._model.addButton(self._reset_button)
        
        # add other buttons if needed. Note that button names must be distinct
        # for all buttons. Events will come back with [buttonname]_press and
        # [buttonname]_release
        
        # Add any timer you have. Multiple timers may be added but they must all
        # have distinct names. Events come back as [timername}_timeout
        #self._timer = SoftwareTimer(name="timer1", handler=None)
        #self._model.addTimer(self._timer)

        # Add any custom events as appropriate for your state model. e.g.
        self._model.addCustomEvent("avg_over_trigger")
        self._model.addCustomEvent("avg_at_or_under_trigger")

        
        # Now add all the transitions from your state model. Any custom events
        # must be defined above first. You can have a state transition to another
        # state based on multiple events - which is why the eventlist is an array
        # Syntax: self._model.addTransition( SOURCESTATE, [eventlist], DESTSTATE)
        
        # some examples:

        #Mens Transitions:
        self._model.addTransition(0, ["button1_press"], 1)
        self._model.addTransition(0, ["button2_press"], 2)
        self._model.addTransition(0, ["button3_press"], 3)

        #womens transitions
        self._model.addTransition(0, ["button4_press"], 1)
        self._model.addTransition(0, ["button5_press"], 2)
        self._model.addTransition(0, ["button6_press"], 3)

        #shared transitions
        self._model.addTransition(1, ["no_event"], 4)
        self._model.addTransition(2, ["no_event"], 4)
        self._model.addTransition(3, ["no_event"], 4)
        self._model.addTransition(4, ["avg_over_trigger"], 0)
        self._model.addTransition(4, ["avg_at_or_under_trigger"], 5)
        self._model.addTransition(5, ["button7_press"], 6)
        self._model.addTransition(6, ["no_event"], 0)


        # etc.

        self._WomensWCList = List(WomensWC)
        self._MensWCList = List(MensWC)

        self._WomensWCFeedbackCollector = LocationFeedbackCollector(WomensWC, self._WomensWCList)  # Pass the list
        self._MensWCFeedbackCollector = LocationFeedbackCollector(MensWC, self._MensWCList)    # Pass the list

        self._alert_threshold = 1.5

        #instantiate LCDDisplay
        self._display = LCDDisplay(sda=16, scl=17)

        #instantiate Buzzers
        self._centralbuzzer = PassiveBuzzer(pin = 20)
        self._mensbuzzer = PassiveBuzzer(pin = 8)
        self._womensbuzzer = PassiveBuzzer(pin = 12)

        #instantiate LightStrip
        self._lightstrip = LightStrip(pin=21, name="LightStrip", numleds=8)

     

    def checkAVG(self):

        """Checks if the new average is > or <= threshold and triggers event.
           Only checks if the list has values.
        """
        womens_avg = self._WomensWCList.average()
        mens_avg = self._MensWCList.average()

        womens_list_has_values = bool(self._WomensWCList.data)
        mens_list_has_values = bool(self._MensWCList.data)

        if womens_list_has_values or mens_list_has_values: # Check if either list has values before averaging
            trigger_alert = (womens_list_has_values and womens_avg <= self._alert_threshold) or \
                            (mens_list_has_values and mens_avg <= self._alert_threshold)

            if trigger_alert:
                self._model.processEvent("avg_at_or_under_trigger")
            else:
                self._model.processEvent("avg_over_trigger")
        else:
            # If neither list has values, do nothing, or potentially transition back to the main display
            # You might want to process a "no_data" event or remain in the current state
            print("No feedback data yet.")  # For debugging
            self._model.processEvent("avg_over_trigger")
    
   
    def notifyManager(self):
        """Notifies manager with audio and visual cues."""

        self._display.showText(f" Check Bathrooms", row=1)
        self._centralbuzzer.play(tone=523)
        time.sleep(.3)
        self._centralbuzzer.stop()
        time.sleep(.3)
        self._centralbuzzer.play(tone=523)
        time.sleep(.3)
        self._centralbuzzer.stop()
        self._lightstrip.setColor(RED)



    
    def showLocationStats(self):
        """Displays the averages for both locations on the LCD."""
        womens_avg = self._WomensWCList.average()
        mens_avg = self._MensWCList.average()

        self._display.clear()
        self._display.showText(f" M:{mens_avg:.1f} W:{womens_avg:.1f}", row=0) #Formatted to 1 decimal places
   

    def systemReset(self):
        """Stops the sound and resets the lists."""
        print("System Reset")
        self._lightstrip.off()
        self._WomensWCList.clear()
        self._MensWCList.clear()
        self.showLocationStats() # Update the display after reset

        
    def stateEntered(self, state, event):
        """
        stateEntered - is the handler for performing entry actions
        You get the state number of the state that just entered
        Make sure actions here are quick
        """
        
        # If statements to do whatever entry/actions you need for
        # for states that have entry actions
        Log.d(f'State {state} entered on event {event}')
        if state == 0:
            # entry actions for state 0
            self.showLocationStats()
        
        elif state == 1: #Unsatisfied
            # entry actions for state 1 Selected for Womens/Mens
            # entry actions for state 1 - Record a 1
            if event == "button4_press":
                self._WomensWCFeedbackCollector.recordFeedback(1)
                self._womensbuzzer.play(196)
                time.sleep(.1)
                self._womensbuzzer.stop()
            elif event == "button1_press":
                self._MensWCFeedbackCollector.recordFeedback(1)
                self._mensbuzzer.play(196)
                time.sleep(.1)
                self._mensbuzzer.stop()
            self._model.processEvent("no_event")

        elif state == 2: #Neutral Selected for Womens/Mens
            # entry actions for state 2 - Record a 2
            if event == "button5_press":
                self._WomensWCFeedbackCollector.recordFeedback(2)
                self._womensbuzzer.play(294)
                time.sleep(.1)
                self._womensbuzzer.stop()
            elif event == "button2_press":
                self._MensWCFeedbackCollector.recordFeedback(2)
                self._mensbuzzer.play(294)
                time.sleep(.1)
                self._mensbuzzer.stop()
            self._model.processEvent("no_event")

        elif state == 3: #Satisfied Selected for Womens/Mens
            # entry actions for state 3 - Record a 3
            if event == "button6_press":
                self._WomensWCFeedbackCollector.recordFeedback(3)
                self._womensbuzzer.play(523)
                time.sleep(.1)
                self._womensbuzzer.stop()
            elif event == "button3_press":
                self._MensWCFeedbackCollector.recordFeedback(3)
                self._mensbuzzer.play(523)
                time.sleep(.1)
                self._mensbuzzer.stop()
            self._model.processEvent("no_event")

        elif state == 4:
            # entry actions for state 4 - Check the averages and transition
            self.showLocationStats()
            self.checkAVG()

        elif state == 5:
            # entry actions for state 5 - Notify Manager
            self.notifyManager()

        elif state == 6:
            # entry actions for state 6 - System Reset
            self.systemReset()
        
            
    def stateLeft(self, state, event):
        """
        stateLeft - is the handler for performing exit/actions
        You get the state number of the state that just entered
        Make sure actions here are quick
        
        This is just like stateEntered, perform only exit/actions here
        """

        Log.d(f'State {state} exited on event {event}')
        if state == 0:
            # exit actions for state 0
            pass
        # etc.
    
    def stateEvent(self, state, event)->bool:
        """
        stateEvent - handler for performing actions for a specific event
        without leaving the current state. 
        Note that transitions take precedence over state events, so if you
        have a transition as well as an in-state action for the same event,
        the in-state action will never be called.

        This handler must return True if the event was processed, otherwise
        must return False.
        """
        
        # Recommend using the debug statement below ONLY if necessary - may
        # generate a lot of useless debug information.
        # Log.d(f'State {state} received event {event}')
        
        # Handle internal events here - if you need to do something
       # if state == 0 and event == 'button1_press':
            # do something for button1 press in state 0 wihout transitioning
            #self._timer.cancel()
           # return True
        
        # Note the return False if notne of the conditions are met
        #return False

    def stateDo(self, state):
        """
        stateDo - the method that handles the do/actions for each state
        """
        
        # Now if you want to do different things for each state that has do actions
        if state == 0:
            # State 0 do/actions
            pass
        elif state == 1:
            # State1 do/actions
            # You can check your sensors here and process events manually if custom events
            # are needed (these must be previously added using addCustomEvent()
            # For example, if you want to go from state 1 to state 2 when the motion sensor
            # is tripped you can do something like this
            # In __init__ - you should have done self._model.addCustomEvent("motion")
            # Here, you check the conditions that should check for this condition
            # Then ask the model to handle the event
            # if self.motionsensor.tripped():
            #    self._model.processEvent("motion")
            pass

    def run(self):
        """
        Create a run() method - you can call it anything you want really, but
        this is what you will need to call from main.py or someplace to start
        the state model.
        """
        
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    def stop(self):
        # The stop method should simply do any cleanup as needed
        # and then call the model's stop method.
        # This removes the button's handlers but will need to see
        # if the IRQ handlers should also be removed
        self._model.stop()
        

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
if __name__ == '__main__':
    p = MyControllerTemplate()
    try:
        p.run()
    except KeyboardInterrupt:
        p.stop()    
