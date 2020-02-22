class CallButton
    def initialize (direction, floor)
        @direction = direction
        @floor = floor
        @light = 'OFF'
    end
end
class Column
    def initialize (id, numberOfFloors, numberofElevators)
        @ID = id
        @elevatorList = []
        @floorList = []
        @callButtonList = []
    
        for x in 0..numberofElevators
            @elevatorList.push(x)
        end
        for x in 0..numberOfFloors
            @floorList.push(x)
        end
        for x in 0..numberOfFloors
            if x != 1
                callbutton = CallButton.new("DOWN", x)
                @callButtonList.push(callbutton)
            end
            if x != numberOfFloors
                callbutton = CallButton.new("UP", x)
                @callButtonList.push(callbutton)
            end
        end
    end
end    

class FloorRequestButon
    def initialize(id)
        @ID = id
        @Pressed = false
    end
end

class Elevator
    def initialize (id, numberOfFloors)
        @ID = id
        @Position = 1
        @Direction = "UP"
        @StopList = []
        @FloorRequestButton = []
        @Door = "Closed"
        @BufferDirection = "UP"
        @BufferList = []

        for i in 0..numberOfFloors
            @FloorRequestButon.push(i)
        end
    end
end
class Controller
    def initialize (howManyColumns, howManyFloors, howManyElevatorsPerColumn)
        @columnList = []

        for i in 0..howManyColumns
            @columnList.push(i)
        end
    end

    def UpdateList (List, Position)
        List.push(Position)
        List.sort
    end
    # finding the elevator which has the shortest stopList and is closer to the user position
    def FindClosestWithShortestListElevator (elevatorsList, userPosition)
        distance = @columnList[0]].floorList.size
        listLength = @columnList[0].floorList.size
        elevatorList.each {|elevator|
            if (elevator.Position - userPosition).abs < distance
                if (elevator.StopList.size <= listLength)
                    listLength = elevator.StopList.size
                    distance = (elevator.Position - userPosition).abs
                    best = elevator
                end
            end
        }
        return best
    end
    def FindTheShortestStopList(elevatorsList)
        istLength = 10
        best = elevatorsList[0]
        elevatorList.each {|elevator|
            l = elevator.StopList.size
            if (l <= listLength)
                listLength = elevator.StopList.size
                best = elevator
            end
        }
        return best
    end

    def RequestElevator(RequestedFloor, Direction)
        var GoodElevators = []
        var BadElevators = []
        puts ("User is at  #{RequestedFloor} and is going  #{Direction}");
        
    end