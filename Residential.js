


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
    Listen(){
        // UNDER CONSTRUCTION
    }
    UpdateList(List, Position, state){
        console.log(List)
        List.push([Position,state]);
        List.sort(function(a, b){return a-b});
    }
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
    RequestElevator(columnID, Position, Direction){
        var GoodElevators = [];
        var BadElevators = [];
        console.log('User is at ' + Position + ' and is going ' + Direction);
        // ###time.sleep
        for (var elevator of this.columnList[columnID - 1].elevatorList){
            console.log('elvator ' + elevator.ID + ' is at ' + elevator.Position + ' floor and its direction is ' + elevator.Direction);
            if (elevator.Position == Position && elevator.Direction == Direction){
                if (elevator.Door == 'OPEN'){
                    this.UpdateList(elevator.StopList, Position, 'IN');
                    console.log('the best elevator No:' + elevator.ID + ' is comming');
                    return elevator;
                }
            }
            else if (Direction == elevator.Direction){
                if (elevator.Direction == 'UP' && elevator.Position < Position){
                    GoodElevators.push(elevator);
                }
                else if ( elevator.Direction == 'DOWN' && elevator.Position > Position){
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
        for (elevator of GoodElevators){
            console.log('Good elevator ID no.' + elevator.ID);
        }
        for (elevator of BadElevators){
            console.log('Good elevator ID no.' + elevator.ID);
        }
        if (GoodElevators.length >= 1) {
            var bestElevator = this.FindClosestWithShortestListElevator(GoodElevators, Position);
            this.UpdateList(bestElevator.StopList, Position, 'IN');
            console.log('the Good2 elevator ' + bestElevator.ID + ' is comming');
            console.log('its stoplist is: ' + bestElevator.StopList)
            return bestElevator;
        }
        else {
            var bestElevator = this.FindTheShortestStopList(BadElevators);
            this.UpdateList(bestElevator.BufferList, Direction);
            bestElevator.BufferDirection = Direction;
            console.log('the Bad2 elevator ' + bestElevator.ID + 'is comming');
            return bestElevator;
        }
    }
    move(elevator){
        while (elevator.StopList.length > 0){
            console.log('stoplit: ' + elevator.StopList + '   - stoplist length: ' + elevator.StopList.length)
            console.log('elevator position: ' + elevator.Position)
            // time.sleep
            if (elevator.StopList[0][0] > elevator.Position){
                elevator.Direction = 'UP';
                while (elevator.Position < elevator.StopList[0][0]){
                    elevator.Position += 1;
                    console.log('Elevator ' + elevator.ID + ' is at floor ' + elevator.Position + 'Floor');
                    // time.sleep
                    if (elevator.Position == this.columnList.length){
                        elevator.Direction = 'IDLE';
                    }
                }
                elevator.Door = 'OPEN';
                console.log('Door is open');
                if (elevator.StopList[0][1] == 'IN'){
                    elevator.StopList.splice(0,1);
                    
                    
                    // RequestedFloor = int(input('input your destionation floor: '))
                    
                }
                else{
                    elevator.StopList.splice(0,1);
                }
            }
            else {
                elevator.Direction = 'DOWN';
                while (elevator.Position > elevator.StopList[0][0]){
                    elevator.Position -= 1;
                    console.log('Elevator ' + elevator.ID + ' is at floor ' + elevator.Position);
                    // time.sleep
                    if (elevator.Position == 1){
                        elevator.Direction = 'IDLE';
                    }
                }
                elevator.Door = 'OPEN';
                console.log('Door is open');
                if (elevator.StopList[0][1] == 'IN'){
                    elevator.StopList.pop();
                    // RequestedFloor = int(input('input your destionation floor: '))
                    // controller.RequestFloor(elevator, RequestedFloor)
                }
                else{
                    elevator.StopList.pop();
                }
            }
            
            // time.sleep(1)
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
        // console.log(elevator.StopList);
        console.log('StopList' + elevator.StopList)
        console.log('requested floor is1111:  ');
        if ((elevator.Direction != 'DOWN' & RequestedFloor > elevator.Position) || (elevator.Direction != 'UP' & RequestedFloor < elevator.Position) || (elevator.StopList.length == 0)){
            this.UpdateList(elevator.StopList, RequestedFloor, 'OUT');
            return;
        }
        else {
            return;
        }
    }   
}

// --- /Classes ----   

// //---- Reading the requested Value from terminal
// const readline = require('readline');

// const rl = readline.createInterface({
// input: process.stdin,
// output: process.stdout
// });
// rl.question('input your destionation floor: ', (answer) => {
//     // TODO: Log the answer in a database
//     console.log(`Requested floor is: ${answer}`);
//     controller.RequestFloor(elevator, answer)
//     rl.close();
// });
// //---- /Reading the requested Value from terminal
                    
const io = require('console-read-write');
io.write('input your destionation floor:  ')
io.write(`the suser is going ${await io.ask('input your destionation floor: ')}!`);





// // ---- Scenario 1 ---
// controller = new Controller(1, 10, 2);
// // console.log('conroller elevator list: ', controller.columnList[0].elevatorList);
//     // --- initializing the elevators ---
// elevator = controller.columnList[0].elevatorList
// elevator[0].Position = 2;
// elevator[0].Direction = 'IDLE';
// elevator[1].Position = 6;
// elevator[1].Direction = 'IDLE';
//     // --- /initializing the elevators ---

//     // --- initializing user ---
// var userPosition = 3;
// var userDirection = 'UP';
// var RequestedFloor = 7;
//     // --- /initializing user ---
// controller.columnList[0].callButtonList[userPosition].Position = userPosition
// controller.columnList[0].callButtonList[userPosition].Direction = userDirection
// commingElevator = controller.RequestElevator(1, controller.columnList[0].callButtonList[userPosition].Position, controller.columnList[0].callButtonList[userPosition].Direction)
// controller.move(commingElevator)
// // ---- /Scenario 1 ---


