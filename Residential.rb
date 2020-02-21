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
        @elevatorList = Array.new
        @floorList = Array.new
        @callButtonList = Array.new
    
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
        @StopList = Array.new
        @FloorRequestButton = Array.new
        @Door = "Closed"
        @BufferDirection = "UP"
        @BufferList = Array.new

        for i in 0..numberOfFloors
            @FloorRequestButon.push(i)
        end
    end
end




