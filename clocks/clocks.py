import datetime
def draw():
    x = datetime.datetime.now()
    x=str(x)
    xx=x.find(".")
    if xx > -1:
        x=x[:xx]
    x= str(x)+"       "
    print(x,end="\r")
    

