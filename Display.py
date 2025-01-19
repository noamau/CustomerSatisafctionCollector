class Display:
    """
    The Display Base class - might not actually be needed
    But here to ensure we do not have a duckTyping problem
    """

    def reset(self):
        Log.e(f"reset NOT IMPLEMENTED in {type(self).__name__}")
        
    def clear(self):
        self.reset()

    def showNumber(self, number):
        Log.e(f"showNumber NOT IMPLEMENTED! in {type(self).__name__}")

    def showText(self, text):
        Log.e(f"showText NOT IMPLEMENTED! in {type(self).__name__}")

    def scroll(self, text, speed=250):
        Log.e(f"Scroll NOT IMPLEMENTED! in {type(self).__name__}")
        
        # Sample code from professor 