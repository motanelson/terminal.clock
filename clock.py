import time
import clocks.clocks
print("\033c\033[40;37m\n")
counter=0
while 1:
    if counter > 100:
         break
    clocks.clocks.draw()
    counter=counter+1
    time.sleep(1)

print("")