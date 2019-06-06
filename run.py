from src.maps.map_context import MapContext
import msvcrt, time

button_delay = 0.2


def run(size):
    while True:
        char = msvcrt.getch()

        if char == "p":
            print("Stop!")
            exit(0)

        if char == "a":
            print("Left pressed")
            time.sleep(button_delay)

        elif char == "d":
            print("Right pressed")
            time.sleep(button_delay)

        elif char == "w":
            print("Up pressed")
            time.sleep(button_delay)

        elif char == "s":
            print("Down pressed")
            time.sleep(button_delay)

        elif char == "1":
            print("Number 1 pressed")
            time.sleep(button_delay)


timeA=time.time()
ctx = MapContext()
timeB=time.time()
ctx.start(2)
timeC=time.time()
ctx.display()
timeD=time.time()
print("overall time: " + str(timeD-timeA))
print("constructor time: " + str(timeB-timeA))
print("start time: " + str(timeC-timeB))
print("display time: " + str(timeD-timeC))
