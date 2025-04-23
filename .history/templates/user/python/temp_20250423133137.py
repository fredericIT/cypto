try:
    temperature=float("fill in")
    if temperature<10:
        print("it  is cold")
    elif temperature>10 and temperature<20:
         print("it is warm")
    elif temperature>20 and temperature<30:
        print("it is hot")
    else:
        print("it is very hot")
except ValueError:
      print("please enter a valid number")