
// --- Classes ----
class CallButton {
    constructor(direction, floor){
        this.direction = direction;
        this.floor = floor;
        this.light = 'OFF'
    }
}
class Column {
    constructor(ID, numberOfFloors, numberOfElevators){
        this.ID = ID;
        this.elevatorList = [];
        this.floorList = [];
        this.callButtonList = [];
        
        for (var i = 1; i <= numberOfElevators; i++) {
            // var elevator = 
            this.elevatorList.push(new Elevator(i , numberOfFloors))
        }
        for (var i = 1; i <= numberOfFloors; i++) {
            this.floorList.push(i)
        }
        for (var i = 1; i <= numberOfFloors; i++) {
            if (i != 1 ){
                var callbutton = new CallButton('DOWN', i)
                this.callButtonList.push(callbutton)
            }
            if (i != numberOfFloors ){
                callbutton = new CallButton('UP', i)
                this.callButtonList.push(callbutton)
            }
        }    
    }
}
class FloorRequestButton {
    constructor(ID){
        this.ID = ID;
        this.Pressed = false;
    }
}
class Elevator {
    constructor(ID, numberOfFloors){
        this.ID = ID;
        this.Position = 1;
        this.Direction = 'UP';
        this.StopList = [];
        this.FloorRequestButton = [];
        this.Door = 'CLOSED';
        this.BufferDirection = 'UP';
        this.BufferList = [];

        for (var i = 1; i <= numberOfFloors; i++){
            this.FloorRequestButton.push(i);
        }
    }
}
class Controller {
    constructor(howManyColumns, howManyFloors, howManyElevatorsPerColumn){
        this.columnList = [];

        for (var i = 1; i <= howManyColumns; i++){
            var column = new Column(i, howManyFloors, howManyElevatorsPerColumn);
            this.columnList.push(column);
        }
    }

    UpdateList(List, Position){
        List.push(Position);
        List.sort(function(a, b){return a-b});
    }
    // finding the elevator which has the shortest stopList and is closer to the user position
    FindClosestWithShortestListElevator (elevatorsList, userPosition){
        var distance = this.columnList[0].floorList.length;
        var best;
        var listLength = this.columnList[0].floorList.length;
        for (var elevator of elevatorsList){
            if (Math.abs(elevator.Position - userPosition) < distance){
                if (elevator.StopList.length <= listLength){
                    listLength = elevator.StopList.length;
                    distance = Math.abs(elevator.Position - userPosition);
                    best = elevator;
                }
            }
        }
        return best;
    }
    FindTheShortestStopList(elevatorsList){
        var listLength = 10;
        var best = elevatorsList[0];
        for (elevator of elevatorsList){
            var l = elevator.StopList.length
            if (l <= listLength){
                listLength = elevator.StopList.length;
                best = elevator;
            }
        }
        return best;
    }
    RequestElevator(RequestedFloor, Direction){
        var GoodElevators = [];
        var BadElevators = [];
        console.log('User is at ' + RequestedFloor + ' and is going ' + Direction);
        for (var elevator of this.columnList[0].elevatorList){
            console.log('elvator ' + elevator.ID + ' is at ' + elevator.Position + ' floor and its direction is ' + elevator.Direction);
            if (elevator.Position == RequestedFloor && elevator.Direction == Direction){
                if (elevator.Door == 'OPEN'){
                    this.UpdateList(elevator.StopList, RequestedFloor);
                    console.log('the best elevator No:' + elevator.ID + ' is comming');
                    return elevator;
                }
            }
            else if (Direction == elevator.Direction){
                if (elevator.Direction == 'UP' && elevator.Position < RequestedFloor){
                    GoodElevators.push(elevator);
                }
                else if ( elevator.Direction == 'DOWN' && elevator.Position > RequestedFloor){
                    GoodElevators.push(elevator);
                }
                else {
                    BadElevators.push(elevator);
                }
            }
            else if (elevator.Direction == 'IDLE'){
                GoodElevators.push(elevator);
            }
            else {
                BadElevators.push(elevator);
            }
        }
        if (GoodElevators.length >= 1) {
            var bestElevator = this.FindClosestWithShortestListElevator(GoodElevators, RequestedFloor);
            this.UpdateList(bestElevator.StopList, RequestedFloor);
            console.log('the elevator ' + bestElevator.ID + ' is comming');
            this.move(bestElevator);
            return bestElevator;
        }
        else {
            var bestElevator = this.FindTheShortestStopList(BadElevators);
            this.UpdateList(bestElevator.BufferList, RequestedFloor);
            bestElevator.BufferDirection = Direction;
            console.log('the elevator ' + bestElevator.ID + 'is comming');
            this.move(bestElevator);
            return bestElevator;
        }
    }
    move(elevator){
        while (elevator.StopList.length > 0){
            if (elevator.StopList[0] > elevator.Position){
                elevator.Direction = 'UP';
                while (elevator.Position < elevator.StopList[0]){
                    elevator.Position += 1;
                    console.log('Elevator ' + elevator.ID + ' is at floor ' + elevator.Position + 'Floor');
                    if (elevator.Position == this.columnList.length){
                        elevator.Direction = 'IDLE';
                    }
                }
                elevator.Door = 'OPEN';
                console.log('Door is open');
                elevator.StopList.splice(0,1);
            }
            else {
                elevator.Direction = 'DOWN';
                while (elevator.Position > elevator.StopList[0]){
                    elevator.Position -= 1;
                    console.log('Elevator ' + elevator.ID + ' is at floor ' + elevator.Position);
                    if (elevator.Position == 1){
                        elevator.Direction = 'IDLE';
                    }
                }
                elevator.Door = 'OPEN';
                console.log('Door is open');
                elevator.StopList.pop();
            }
            
            elevator.Door = 'CLOSED';
            console.log('Door is closed');
            elevator.Direction = 'IDLE';
        }
        if (elevator.BufferList.length > 0){
            elevator.StopList = eleavtor.BufferList;
            elevator.Direction = elevator.BufferDirection;
            elevator.BufferList = [];
            this.move(elevator);
        }
        else {
            elevator.Direction = 'IDLE';
        }
    }
    RequestFloor(elevator, RequestedFloor){
        
        this.UpdateList(elevator.StopList, RequestedFloor);
        this.move(elevator);
        return;
    }   
}
// --- /Classes ----   


// --- Scenarios ---
function Scenario1(){
    console.log('******************* ******************* *******************');
    console.log('*******************      Scenario 1     *******************');
    console.log('******************* ******************* *******************');
    controller1 = new Controller(1, 10, 2);

    controller1.columnList[0].elevatorList[0].Position = 2;
    controller1.columnList[0].elevatorList[0].Direction = 'IDLE';
    controller1.columnList[0].elevatorList[1].Position = 6;
    controller1.columnList[0].elevatorList[1].Direction = 'IDLE';
    console.log('******************* USER-1 goes from floor 3 to floor 7  *******************');
    RequestedFloor = 3;
    Direction = 'UP';
    Destination = 7;

    elevator = controller1.RequestElevator(RequestedFloor, Direction);
    controller1.RequestFloor(elevator, Destination);
}
function Scenario2(){
    console.log('******************* ******************* *******************');
    console.log('*******************      Scenario 2     *******************');
    console.log('******************* ******************* *******************');
    controller2 = new Controller(1, 10, 2);

    controller2.columnList[0].elevatorList[0].Position = 10;
    controller2.columnList[0].elevatorList[0].Direction = 'IDLE';
    controller2.columnList[0].elevatorList[1].Position = 3;
    controller2.columnList[0].elevatorList[1].Direction = 'IDLE';


    console.log('******************* USER-1 goes from floor 1 to floor 6  *******************');
    RequestedFloor = 1;
    Direction = 'UP';
    Destination = 6;


    elevator = controller2.RequestElevator(RequestedFloor, Direction);
    controller2.RequestFloor(elevator, Destination);

    console.log('******************* USER-2 goes from floor 3 to floor 5  *******************');
    RequestedFloor = 3;
    Direction = 'UP';
    Destination = 5;


    elevator = controller2.RequestElevator(RequestedFloor, Direction);
    controller2.RequestFloor(elevator, Destination);

    console.log('******************* USER-3 goes from floor 9 to floor 2  *******************');
    RequestedFloor = 9;
    Direction = 'DOWN';
    Destination = 2;


    elevator = controller2.RequestElevator(RequestedFloor, Direction);
    controller2.RequestFloor(elevator, Destination);
}
function Scenario3(){
    console.log('******************* ******************* *******************');
    console.log('*******************      Scenario 3     *******************');
    console.log('******************* ******************* *******************');
    controller3 = new Controller(1, 10, 2);

    controller3.columnList[0].elevatorList[0].Position = 10;
    controller3.columnList[0].elevatorList[0].Direction = 'IDLE';
    controller3.columnList[0].elevatorList[1].Position = 3;
    controller3.columnList[0].elevatorList[1].Direction = 'UP';
    controller3.columnList[0].elevatorList[1].StopList.push(6);


    console.log('******************* USER-1 goes from floor 3 to floor 2  *******************');
    RequestedFloor = 3;
    Direction = 'DOWN';
    Destination = 2;

    elevator = controller3.RequestElevator(RequestedFloor, Direction);
    controller3.RequestFloor(elevator, Destination);

    console.log('moving eleavtor 2 from floor 3 to floor 6');
    controller3.move(controller3.columnList[0].elevatorList[1]);

    console.log('******************* USER-2 goes from floor 10 to floor 3  *******************');
    RequestedFloor = 10;
    Direction = 'DOWN';
    Destination = 3;

    elevator = controller3.RequestElevator(RequestedFloor, Direction);
    controller3.RequestFloor(elevator, Destination);
}
//  --- /Scenarios---

// --- Main PRogram ---
Scenario1();
// Scenario2();
// Scenario3();
// --- /Main PRogram ---
