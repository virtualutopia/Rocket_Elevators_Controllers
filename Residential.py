import time

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
                callbutton = CallButton('DOWN', i)
                self.callButtonList.append(callbutton)

            if i != numberOfFloors :
                callbutton = CallButton('UP', i)
                self.callButtonList.append(callbutton)

class FloorRequestButton():
    def __init__(self, ID):
        self.ID = ID
        self.Pressed = False

class Elevator():
    def __init__(self, ID, numberOfFloors):
        self.ID = ID
        self.Position = 1
        self.Direction = 'UP'
        self.StopList = [] 
        self.FloorRequestButton = []
        self.Door = 'CLOSED'
        self.BufferDirection = 'UP'
        self.BufferList = []

        for i in range (numberOfFloors):
            self.FloorRequestButton.append(i)


class Controller():
    def __init__ (self, howManyColumns, howManyFloors, howManyElevatorsPerColumn):
        self.columnList = []
        for i in range(howManyColumns):
            self.columnList.append(Column(i +1, howManyFloors, howManyElevatorsPerColumn))

    # The method Listen is not used in the SCENARIOs but it is used when the program is runned on AUTOMATED version

            
    def UpdateList(self, elList, Position):
        elList.append(Position)
        elList.sort()
    # finding the elevator which has the shortest stopList and is closer to the user position
    def FindClosestWithShortestListElevator(self, elevatorsList, userPosition):
        distance = len(self.columnList[0].floorList)
        best = elevatorsList[0]
        listLength = 10
        for elevator in elevatorsList:
            if abs(elevator.Position - userPosition) < distance:
                if len(elevator.StopList) <= listLength:
                    listLength = len(elevator.StopList)
                    best = elevator
                    distance = abs(elevator.Position - userPosition)
        return best
    def FindTheShortestStopList(self, elevatorsList):
        listLength = 10
        best = elevatorsList[0]
        for elevator in elevatorsList:
            if len(elevator.StopList) < listLength:
                listLength = len(elevator.StopList)
                best = elevator
        return best
    def RequestElevator(self, RequestedFloor, Direction):
        GoodElevators = []
        BadElevators = []
        for elevator in self.columnList[0].elevatorList:
            print ('elvator', elevator.ID, ' is at floor ', elevator.Position, ' and its direction is ', elevator.Direction)
            if (elevator.Position == RequestedFloor and elevator.Direction == Direction) :
                if (elevator.Door == 'OPEN'):
                    self.UpdateList(elevator.StopList, RequestedFloor)
                    print('the elevator', elevator.ID, ' is comming')
                    self.move(elevator)
                    return elevator
            elif (Direction == elevator.Direction):
                if (elevator.Direction == 'UP' and elevator.Position < RequestedFloor):
                    GoodElevators.append(elevator)
                elif (elevator.Direction == 'DOWN' and elevator.Position > RequestedFloor):
                    GoodElevators.append(elevator)
                else:
                    BadElevators.append(elevator)
            elif (elevator.Direction == 'IDLE'):
                GoodElevators.append(elevator)
            else:
                BadElevators.append(elevator)

        if len(GoodElevators) >= 1:
            bestElevator = self.FindClosestWithShortestListElevator(GoodElevators, RequestedFloor)
            self.UpdateList(bestElevator.StopList, RequestedFloor)
            print('the elevator', bestElevator.ID, ' is comming')
            self.move(bestElevator)
            return bestElevator
        else :
            bestElevator = self.FindTheShortestStopList(BadElevators)
            self.UpdateList(bestElevator.BufferList, RequestedFloor)
            bestElevator.BufferDirection = Direction
            print('the elevator', bestElevator.ID, ' is comming')
            self.move(bestElevator)
            return bestElevator
    
    def move(self, elevator):
        while (len(elevator.StopList) > 0) :
            if (elevator.StopList[0] > elevator.Position) :
                elevator.Direction = 'UP'
                while (elevator.Position < elevator.StopList[0]):
                    elevator.Position += 1
                    print('Elevator ', elevator.ID, ' is at Floor ', elevator.Position)
                    time.sleep(.5)
                    
                    if (elevator.Position == len(self.columnList)):
                        elevator.Direction = 'IDLE'
                elevator.Door = 'OPEN'
                print('Door is open')
                elevator.StopList.pop(0)
            else:
                elevator.Direction = 'DOWN'
                while (elevator.Position > elevator.StopList[0]):
                    elevator.Position -= 1
                    print('Elevator ', elevator.ID, ' is at Floor ', elevator.Position)
                    time.sleep(.5)
                    if (elevator.Position == 1):
                        elevator.Direction = 'IDLE'
                elevator.Door = 'OPEN'
                print('Door is open')
                elevator.StopList.pop(len(elevator.StopList) - 1)
            time.sleep(.5)
            elevator.Door = 'CLOSED'
            print('Door is closed')
            elevator.Direction = 'IDLE'

        if (len(elevator.BufferList) > 0) :
            elevator.StopList = elevator.BufferList
            elevator.Direction = elevator.BufferDirection
            elevator.BufferList = []
            self.move(elevator)
        else :
            elevator.direction = 'IDLE'

    def RequestFloor(self, elevator, RequestedFloor):
            self.UpdateList(elevator.StopList, RequestedFloor)
            self.move(elevator)
            return
# --- /Classes ---



# # --- Scenarios ---
def Scenario1 ():
    print('******************* ******************* *******************')
    print('*******************      Scenario 1     *******************')
    print('******************* ******************* *******************')
    controller1 = Controller(1, 10, 2)

    controller1.columnList[0].elevatorList[0].Position = 2
    controller1.columnList[0].elevatorList[0].Direction = 'IDLE'
    controller1.columnList[0].elevatorList[1].Position = 6
    controller1.columnList[0].elevatorList[1].Direction = 'IDLE'
    print('******************* USER-1 goes from floor 3 to floor 7  *******************')
    RequestedFloor = 3
    Direction = 'UP'
    Destination = 7

    elevator = controller1.RequestElevator(RequestedFloor, Direction)
    controller1.RequestFloor(elevator, Destination)

def Scenario2 ():
    print('******************* ******************* *******************')
    print('*******************      Scenario 2     *******************')
    print('******************* ******************* *******************')
    controller2 = Controller(1, 10, 2)

    controller2.columnList[0].elevatorList[0].Position = 10
    controller2.columnList[0].elevatorList[0].Direction = 'IDLE'
    controller2.columnList[0].elevatorList[1].Position = 3
    controller2.columnList[0].elevatorList[1].Direction = 'IDLE'


    print('******************* USER-1 goes from floor 1 to floor 6  *******************')
    RequestedFloor = 1
    Direction = 'UP'
    Destination = 6



    elevator = controller2.RequestElevator(RequestedFloor, Direction)
    controller2.RequestFloor(elevator, Destination)

    print('******************* USER-2 goes from floor 3 to floor 5  *******************')
    RequestedFloor = 3
    Direction = 'UP'
    Destination = 5


    elevator = controller2.RequestElevator(RequestedFloor, Direction)
    controller2.RequestFloor(elevator, Destination)

    print('******************* USER-3 goes from floor 9 to floor 2  *******************')
    RequestedFloor = 9
    Direction = 'DOWN'
    Destination = 2


    elevator = controller2.RequestElevator(RequestedFloor, Direction)
    controller2.RequestFloor(elevator, Destination)

def Scenario3 ():
    print('******************* ******************* *******************')
    print('*******************      Scenario 3     *******************')
    print('******************* ******************* *******************')
    controller3 = Controller(1, 10, 2)

    controller3.columnList[0].elevatorList[0].Position = 10
    controller3.columnList[0].elevatorList[0].Direction = 'IDLE'
    controller3.columnList[0].elevatorList[1].Position = 3
    controller3.columnList[0].elevatorList[1].Direction = 'UP'
    controller3.columnList[0].elevatorList[1].StopList.append(6)


    print('******************* USER-1 goes from floor 3 to floor 2  *******************')
    RequestedFloor = 3
    Direction = 'DOWN'
    Destination = 2

    elevator = controller3.RequestElevator(RequestedFloor, Direction)
    controller3.RequestFloor(elevator, Destination)

    print('moving eleavtor 2 from floor 3 to floor 6')
    controller3.move(controller3.columnList[0].elevatorList[1])

    print('******************* USER-2 goes from floor 10 to floor 3  *******************')
    RequestedFloor = 10
    Direction = 'DOWN'
    Destination = 3

    elevator = controller3.RequestElevator(RequestedFloor, Direction)
    controller3.RequestFloor(elevator, Destination)
# # --- /Scenarios ---


# --- Main PRogram ---
# Scenario1()
Scenario2()
# Scenario3()

# --- Main PRogram ---
