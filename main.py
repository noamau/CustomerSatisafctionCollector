import time
from CentralController import *
time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

c = CentralController()
c.run()


