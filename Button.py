class Button:
    def __init__(self, pin, name, *, handler=None, lowActive=True):
        """
        Initialize attributes and other internal data
        """
        
        self._pinNo = pin
        self._name = name
        Log.i(f'Button constructor: create button {name} at pin {pin}')
        if lowActive:
            self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        else:
            self._pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self._debounce_time = 0
        self._lowActive = lowActive
        self._lastStatus = None
        self._handler = None
        self.setHandler(handler)
        
        # Sample code from professor 