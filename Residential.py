# Residential Controller 
import random
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
        # self.State = 'IDLE'
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


    def Listen(self):
        while True:
            try:
                x = int(input('Which floor are you calling from?   : '))
            except ValueError:
                print('ERROR::: enter a vlid number!')
            if (x >= 1 and x <= len(self.columnList[0].floorList)) :
                self.columnList[0].callButtonList[x].Position = int(x)
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
                    self.columnList[0].callButtonList[x].Direction = 'UP'
                    break
                elif (dir in ['d', 'D', 'down', 'Down', 'DOWN']):
                    self.columnList[0].callButtonList[x].Direction = 'DOWN'
                    break
            else:
                print('ERROR::: enter a vlid direction (U/D)!')
            
        return self.columnList[0].callButtonList[x]
            
    def UpdateList(self, elList, Position, state):
        elList.append([Position, state])
        elList.sort()
    # finding the elevator which has the shortest stopList and is closer to the user position
    def FindClosestWithShortestListElevator(self, elevatorsList, userPosition):
        # print ('FindClosestWithShortestListElevator elevators: ', elevators)
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
    def RequestElevator(self, columnID, Position, Direction):
        #  print('user is here: ', Position, 'and going ',Direction)
        GoodElevators = []
        BadElevators = []
        print ('User is at ', Position, ' and is goind', Direction)
        for elevator in self.columnList[columnID - 1].elevatorList:
            print ('elvator', elevator.ID, ' is at floor ', elevator.Position, ' and its direction is ', elevator.Direction)
            time.sleep(.3)
            # the first condition (if) is the ideal case and rarely happens 
            if (elevator.Position == Position and elevator.Direction == Direction) :
                if (elevator.Door == 'OPEN'):
                    self.UpdateList(elevator.StopList, Position, 'IN')
                    print('the elevator', elevator.ID, ' is comming')
                    return elevator
            # Usually the following cases happen
            elif (Direction == elevator.Direction):
                if (elevator.Direction == 'UP' and elevator.Position < Position):
                    GoodElevators.append(elevator)
                    # print('el no', elevator.ID, 'added to GOOD1')
                elif (elevator.Direction == 'DOWN' and elevator.Position > Position):
                    GoodElevators.append(elevator)
                    # print('el no', elevator.ID, 'added to GOOD2')
                else:
                    BadElevators.append(elevator)
            # other probable case: Elevator is IDLE
            elif (elevator.Direction == 'IDLE'):
                GoodElevators.append(elevator)
                # print('el no', elevator.ID, 'added to GOOD3')
            # the worse case depening on elevator direction and position, elevator will be added to BADLIST
            else:
                BadElevators.append(elevator)
                # print('el no', elevator.ID, 'added to BAD2')

        if len(GoodElevators) >= 1:
            # print('GOOD elevators')
            # for i in range(len(GoodElevators)):
            #     print ('el no. ', GoodElevators[i].ID)
            bestElevator = self.FindClosestWithShortestListElevator(GoodElevators, Position)
            self.UpdateList(bestElevator.StopList, Position, 'IN')
            print('the elevator', bestElevator.ID, ' is comming')
            # print('the elevator', bestElevator.ID, ' is comming')
            return bestElevator
        else :
            # print('BAD elevators')
            # for i in range(len(BadElevators)):
            #     print ('el no. ', BadElevators[i].ID)
            bestElevator = self.FindTheShortestStopList(BadElevators)
            self.UpdateList(bestElevator.BufferList, Position, 'IN')
            bestElevator.BufferDirection = Direction
            print('the elevator', bestElevator.ID, ' is comming')
            # print('the badelevator', bestElevator.ID, ' is comming')
            return bestElevator
    
    def move(self, elevator):
        # print('elevator1: ', elevator)
        # print('length stoplist: ', len(elevator.StopList))
        while (len(elevator.StopList) > 0) :
            # print('stops: ', elevator.StopList) 
            time.sleep(3)
            if (elevator.StopList[0][0] > elevator.Position) :
                elevator.Direction = 'UP'
                while (elevator.Position < elevator.StopList[0][0]):
                    elevator.Position += 1
                    print('Elevator ', elevator.ID, ' is at Floor ', elevator.Position)
                    time.sleep(1)
                    if (elevator.Position == len(self.columnList)):
                        elevator.Direction = 'IDLE'
                elevator.Door = 'OPEN'
                print('Door is open')
                if (elevator.StopList[0][1] == 'IN'):
                    elevator.StopList.pop(0)
                    RequestedFloor = int(input('input your destionation floor: '))
                    controller.RequestFloor(elevator, RequestedFloor)
                else:
                    elevator.StopList.pop(0)
            else:
                elevator.Direction = 'DOWN'
                while (elevator.Position > elevator.StopList[0][0]):
                    elevator.Position -= 1
                    print('Elevator ', elevator.ID, ' is at Floor ', elevator.Position)
                    time.sleep(1)
                    if (elevator.Position == 1):
                        elevator.Direction = 'IDLE'
                elevator.Door = 'OPEN'
                print('Door is open')
                if (elevator.StopList[0][1] == 'IN'):
                    elevator.StopList.pop(len(elevator.StopList) - 1)
                    RequestedFloor = int(input('input your destionation floor: '))
                    # print('requestedFloor: ', RequestedFloor)
                    controller.RequestFloor(elevator, RequestedFloor)
                else:
                    elevator.StopList.pop(len(elevator.StopList) - 1)
            time.sleep(1)
            elevator.Door = 'CLOSED'
            print('Door is closed')
            elevator.Direction = 'IDLE'

        if (len(elevator.BufferList) > 0) :
            # print('stoplist: ', elevator.StopList)
            # print('bufferlist: ', elevator.BufferList)
            elevator.StopList = elevator.BufferList
            # for i in range(len(elevator.BufferList) - 1) :
            #     elevator.StopList[i] = elevator.BufferList[i]
            #     print('stop ', elevator.StopList[i], 'buffer ', elevator.BufferList[i])
            elevator.Direction = elevator.BufferDirection
            elevator.BufferList = []
            # print('stoplist: ', elevator.StopList)
            # print('stoplist: ', elevator.BufferList)
            self.move(elevator)
        else :
            elevator.direction = 'IDLE'
        # else :
            # while (elevator.Position <= len(column.floorList) or len(elevator.BufferList) > 0):
            #         if elevator.BufferList == 'UP' :
            #             elevator.Position += 1
            #         else :
            #             elevator.Position -= 1
            #         print('Elevator ', elevator.ID, ' is at ', elevator.Position, 'Floor')
            #         time.sleep(1)
            # elevator.Door = 'OPEN'
            # print('Door is open')
            # time.sleep(1)
            # elevator.Door = 'CLOSED'
            # print('Door is closed')

    def RequestFloor(self, elevator, RequestedFloor):
        # print('requestedFloor: ', RequestedFloor, 'elevatorID: ', elevator.ID, elevator.StopList)
        if (elevator.Direction != 'DOWN' and RequestedFloor > elevator.Position) or (elevator.Direction != 'UP' and RequestedFloor < elevator.Position) or (len(elevator.StopList) == 0):
            self.UpdateList(elevator.StopList, RequestedFloor, 'OUT')
            # print('elevatorID: ', elevator.ID, elevator.StopList)
            return
        else :
            return 
# --- /Classes ---



# # --- NO SCENARIO - AUTOMATED VERSION ---
# controller = Controller(1, 10, 3)
# # --- Initialization of the elevators --- 
# for j in range (len(controller.columnList)):
#     for i in range (len(controller.columnList[j].elevatorList)) :
#         controller.columnList[j].elevatorList[i].Position = random.randint(1, len(controller.columnList[j].floorList))
#         controller.columnList[j].elevatorList[i].StopList.append([random.randint(1, 10), 'OUT'])
#         if (controller.columnList[j].elevatorList[i].StopList[0][0] > controller.columnList[j].elevatorList[i].Position) :
#             controller.columnList[j].elevatorList[i].Direction = 'UP'
#         else : 
#             controller.columnList[j].elevatorList[i].Direction = 'DOWN'
#         random.seed((i + 10) * 10)
# # --- /Initialization of the elevators --- 
# callButton = controller.Listen()
# commingElevator = controller.RequestElevator(1, callButton.Position, callButton.Direction)
# controller.move(commingElevator)
# # --- /NO SCENARIO - AUTOMATED VERSION ---

# # # --- Scenario 1 ---
# controller = Controller(1, 10, 2)

# controller.columnList[0].elevatorList[0].Position = 2
# controller.columnList[0].elevatorList[0].Direction = 'IDLE'
# controller.columnList[0].elevatorList[1].Position = 6
# controller.columnList[0].elevatorList[1].Direction = 'IDLE'
# userPosition = 3
# userDirection = 'UP'
# userDestination = 7

# controller.columnList[0].callButtonList[userPosition].Position = userPosition
# controller.columnList[0].callButtonList[userPosition].Direction = userDirection

# print('******************* Scenario 1  *******************')
# print('******************* USER-1 goes from floor 3 to floor 7  *******************')
# commingElevator = controller.RequestElevator(1, controller.columnList[0].callButtonList[userPosition].Position, controller.columnList[0].callButtonList[userPosition].Direction)
# controller.move(commingElevator)

# # # --- /Scenario 1 ---

# # --- Scenario 2 ---
controller = Controller(1, 10, 2)

controller.columnList[0].elevatorList[0].Position = 10
controller.columnList[0].elevatorList[0].Direction = 'IDLE'
controller.columnList[0].elevatorList[1].Position = 3
controller.columnList[0].elevatorList[1].Direction = 'IDLE'

print('****** 1st user at Floor 1 ******')
userPosition = 1
userDirection = 'UP'
userDestination = 6

controller.columnList[0].callButtonList[userPosition].Position = userPosition
controller.columnList[0].callButtonList[userPosition].Direction = userDirection
print('******************* Scenario 2 *******************');
print('******************* USER-1 goes from floor 3 to floor 6  *******************')
commingElevator = controller.RequestElevator(1, controller.columnList[0].callButtonList[userPosition].Position, controller.columnList[0].callButtonList[userPosition].Direction)
controller.move(commingElevator)
print('****** 2nd user at Floor 3 ******')
print('****** 2nd user at Floor 3 ******')
userPosition = 3
userDirection = 'UP'
userDestination = 5

controller.columnList[0].callButtonList[userPosition].Position = userPosition
controller.columnList[0].callButtonList[userPosition].Direction = userDirection
print('******************* USER-2 goes from floor 3 to floor 5  *******************')
commingElevator = controller.RequestElevator(1, controller.columnList[0].callButtonList[userPosition].Position, controller.columnList[0].callButtonList[userPosition].Direction)
controller.move(commingElevator)

print('****** 3rd user at Floor 9 ******')
print('****** 3rd user at Floor 9 ******')
userPosition = 9
userDirection = 'DOWN'
userDestination = 2
print('******************* USER-3 goes from floor 9 to floor 2  *******************')
controller.columnList[0].callButtonList[userPosition].Position = userPosition
controller.columnList[0].callButtonList[userPosition].Direction = userDirection

commingElevator = controller.RequestElevator(1, controller.columnList[0].callButtonList[userPosition].Position, controller.columnList[0].callButtonList[userPosition].Direction)
controller.move(commingElevator)

# # --- /Scenario 2 ---


# # --- Scenario 3 ---

# controller = Controller(1, 10, 2)

# controller.columnList[0].elevatorList[0].Position = 10
# controller.columnList[0].elevatorList[0].Direction = 'IDLE'
# controller.columnList[0].elevatorList[1].Position = 3
# controller.columnList[0].elevatorList[1].Direction = 'UP'
# controller.columnList[0].elevatorList[1].StopList.append([6,'OUT'])

# print('****** 1st user at Floor 1 ******')
# userPosition = 3
# userDirection = 'DOWN'
# userDestination = 2

# controller.columnList[0].callButtonList[userPosition].Position = userPosition
# controller.columnList[0].callButtonList[userPosition].Direction = userDirection
# print('******************* Scenario 3 *******************')
# print('******************* USER-1 goes from floor 3 to floor 2  *******************')
# commingElevator = controller.RequestElevator(1, controller.columnList[0].callButtonList[userPosition].Position, controller.columnList[0].callButtonList[userPosition].Direction)
# controller.move(commingElevator)
# # moving eleavtor 2 from floor 3 to floor 6
# controller.move(controller.columnList[0].elevatorList[1])

# print('****** 2nd user at Floor 10 ******')
# print('****** 2nd user at Floor 10 ******')
# userPosition = 10
# userDirection = 'DOWN'
# userDestination = 3
# print('******************* USER-2 goes from floor 10 to floor 3  *******************')
# controller.columnList[0].callButtonList[userPosition].Position = userPosition
# controller.columnList[0].callButtonList[userPosition].Direction = userDirection

# commingElevator = controller.RequestElevator(1, controller.columnList[0].callButtonList[userPosition].Position, controller.columnList[0].callButtonList[userPosition].Direction)
# controller.move(commingElevator)

# # --- /Scenario 3 ---


