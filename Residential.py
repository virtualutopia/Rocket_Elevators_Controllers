# Residential Controller 
import random
import time

# --- Constants ---
# numberOfElevators = 3
# numberOfFloors = 10
# --- /Constants ---


# --- Main  ---
def main():
    callButton = Listen()
    RequestElevator(callButton.Position, callButton.Direction)
    RequestFloor()
 
# --- /Main  ---
   



# --- Classes ---


class CallButton():
    def __init__(self, direction, floor):
        self.direction = direction
        self.floor = floor
        self.light = 'OFF'

class Column():
    def __init__(self, ID, numberOfFloors, numberOfElevators):
        self.ID = ID
        self.elevatorList = []
        self.floorList = []
        self.callButtonList = []
        
        for i in range (numberOfElevators):
            elevator = Elevator(i + 1, numberOfFloors)
            self.elevatorList.append(elevator)

        for i in range (numberOfFloors):
            self.floorList.append(i)

        for i in range (numberOfFloors):
            if i != 1 :
                callbutton = CallButton('Down', i)
                self.callButtonList.append(callbutton)
            if i != numberOfFloors :
                callbutton = CallButton('Down', i)
                self.callButtonList.append(callbutton)

class FloorRequestButton():
    def __init__(self, ID):
        self.ID = ID
        self.Pressed = False

class Elevator(object):
    def __init__(self, ID, numberOfFloors):
        self.ID = ID
        # self.State = 'IDLE'
        self.Position = 1
        self.Direction = 'UP'
        self.StopList = [] 
        self.FloorRequestButton = []
        self.Door = 'CLOSED'
        self.BufferDirection = 'UP'
        self.BufferList = []

        for i in range (numberOfFloors):
            floorRequestButton = FloorRequestButton (i)
            self.FloorRequestButton.append(floorRequestButton)
    def move(self, Direction, NextStop):
        pass
        # 
        # to be defined
        # 
class User(object):
    def __init__ (self, Position, Direction):
        self.Position = Position
        self.Direction = Direction

def Listen():
    # for i in range (len(column.callButtonList)):
    #     if column.callButtonList[i].light == 'ON':
    #         return (column.callButtonList[i])
    while True:
        try:
            x = int(input('Which floor are you calling from?   : '))
        except ValueError:
            print('ERROR::: enter a vlid number!')
        if (x >= 1 and x <= len(column.floorList)) :
            column.callButtonList[x].Position = int(x)
            break
        else:
            print('ERROR::: enter a vlid number!') 
        
    
    while True:
        try:
            dir = input('What is your direction(U/D)?  : ')
        except ValueError:
            print('ERROR::: enter a vlid number!')
        if (dir in ['u', 'U', 'up', 'UP', 'Up', 'd', 'D', 'down', 'Down', 'DOWN']):
            if (dir in ['u', 'U', 'up', 'UP', 'Up']):
                column.callButtonList[x].Direction = 'UP'
                break
            elif (dir in ['d', 'D', 'down', 'Down', 'DOWN']):
                column.callButtonList[x].Direction = 'DOWN'
                break
        else:
            print('ERROR::: enter a vlid direction (U/D)!')
        
    # print('user is here: ', x, 'and going ',column.callButtonList[x].Direction)
    return column.callButtonList[x]
            
def UpdateList(List, Position):
    List.append(Position)
    List.sort()
# finding the elevator which has the shortest stopList and is closer to the user position
def FindBesttElevator(elevators, userPosition):
    distance = len(column.floorList)
    # print ('FindBesttElevator elevators: ', elevators)
    best = elevators[0]
    listLength = 10
    for elevator in elevators:
        if abs(elevator.Position - userPosition) < distance:
            if len(elevator.StopList) < listLength:
                listLength = len(elevator.StopList)
                best = elevator
    return best
def findTheShortestStopList(elevators, userPosition):
    listLength = 10
    best = elevators[0]
    for elevator in elevators:
        if len(elevator.StopList) < listLength:
            listLength = len(elevator.StopList)
            best = elevator
    return best
def RequestElevator(Position, Direction):
    #  print('user is here: ', Position, 'and going ',Direction)
    GoodElevators = []
    BadElevators = []
    print ('User is at ', Position, ' and is goind', Direction)
    for elevator in column.elevatorList:
        print ('elvator ID', elevator.ID, 'elevator.Position', elevator.Position, 'elevator.Direction', elevator.Direction)
        time.sleep(.3)
        if (elevator.Position == Position and elevator.Direction == Direction) :
            if (elevator.Door == 'OPEN'):
                UpdateList(elevator.StopList, Position)
                print('the BEST elevator', elevator.ID, ' is comming')
                return 
        elif (Direction == elevator.Direction):
            if (elevator.Direction == 'UP' and elevator.Position < Position):
                GoodElevators.append(elevator)
                print('el no', elevator.ID, 'added to GOOD1')
            elif (elevator.Direction == 'DOWN' and elevator.Position > Position):
                GoodElevators.append(elevator)
                print('el no', elevator.ID, 'added to GOOD2')
        elif (elevator.Direction == 'IDLE'):
            GoodElevators.append(elevator)
            print('el no', elevator.ID, 'added to GOOD3')
        else:
            BadElevators.append(elevator)
            print('el no', elevator.ID, 'added to BAD')

    if len(GoodElevators) >= 1:
        print('GOOD elevators')
        for i in range(len(GoodElevators)):
            print ('el no. ', GoodElevators[i].ID)
        bestElevator = FindBesttElevator(GoodElevators, Position)
        UpdateList(bestElevator.StopList, Position)
        print('the GOOD elevator', bestElevator.ID, ' is comming')
        return
    else :
        print('BAD elevators')
        for i in range(len(BadElevators)):
            print ('el no. ', BadElevators[i].ID)
        bestElevator = findTheShortestStopList(BadElevators, Position)
        UpdateList(bestElevator.BufferList, Position)
        bestElevator.BufferDirection = Direction
        print('the BAD elevator', bestElevator.ID, ' is comming')
        return
    
def RequestFloor():
    pass
# --- /Classes ---


column = Column(1, 10, 3)
# --- Initialization of the elevators --- 
for i in range (len(column.elevatorList)) :
    column.elevatorList[i].Position = random.randint(1, len(column.floorList))
    checkList1 = ['UP', 'DOWN']
    column.elevatorList[i].Direction = random.choice(checkList1)
    time.sleep(.1)
    random.seed((i + 10) * 10)
    # --- /Initialization of the elevators --- 
user = User(1,1)
main()
