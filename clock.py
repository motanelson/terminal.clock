import time
import os
import datetime
def draw():
    x = datetime.datetime.now()
    x=str(x)
    xx=x.find(".")
    if xx > -1:
        x=x[:xx]
    x= str(x)+"       "
    print(x,end="\r")
    

print("\033c\033[40;37m\n")
counter=0
while 1:
    if counter > 100:
         break
    draw()
    counter=counter+1
    time.sleep(1)

print("")