using System;
using System.Collections.Generic;
using System.Linq;

namespace Rocket_Elevators_Controllers
{
    class CallButton
    {
        public string Direction;
        public int Floor;
        public string Light;

        public CallButton(string d, int f)
        {
            this.Direction = d;
            this.Floor = f;
            this.Light = "OFF";
        }
        public string direction
        {
            get { return Direction; }
            set { Direction = value; }
        }
        public int floor
        {
            get { return floor; }
            set { floor = value; }
        }
    }
    class FloorRequestButton
    {
        public int ID;
        public bool Pressed = false;

        public FloorRequestButton(int ID)
        {
            this.ID = ID;
        }
        public int id
        {
            get { return ID; }
            set { ID = value; }
        }
    }
    class Elevator
    {
        public int ID;
        public int Position = 1;
        public string Direction = "UP";
        public List<int> StopList = new List<int>();
        public List<int> floorList = new List<int>();
        public string Door = "CLOSED";
        public string BufferDirection = "UP";
        public List<int> BufferList = new List<int>();
        public Elevator(int ID, int fromFloor, int toFloor)
        {
            this.ID = ID;
            for (int i = fromFloor; i <= toFloor; i = i + 1)
            {
                this.floorList.Add(i);
            }
        }
    }

    class Column
    {
        public int ID;
        public List<Elevator> elevatorList = new List<Elevator>();
        public List<int> floorList = new List<int>();
        public List<CallButton> callButonList = new List<CallButton>();
        // public int fromFloor;
        // public int numberOfFloors;
        // public int numberOfElevators;
        public Column(int ID, int fromFloor, int toFloor, int numberOfElevators)
        {
            this.ID = ID;
            this.floorList.Add(1);
            for (int i = fromFloor; i <= toFloor; i = i + 1)
            {
                this.floorList.Add(i);
            }
            for (int i = 1; i <= numberOfElevators; i = i + 1)
            {
                this.elevatorList.Add(new Elevator(i, fromFloor, toFloor));
            }
            if (ID == 1)
            {
                for (int i = toFloor; i <= fromFloor; i = i + 1)
                {
                    CallButton callButton = new CallButton("UP", i);
                    this.callButonList.Add(callButton);
                }
            }
            else
            {
                for (int i = fromFloor; i <= (toFloor); i = i + 1)
                {
                    CallButton callButton = new CallButton("DOWN", i);
                    this.callButonList.Add(callButton);
                }
            }
            Console.WriteLine("ColumnID: " + this.ID.ToString() + " sopports these floors: " + string.Join(" | ", this.floorList));
        }
    }
    class Battery
    {
        public List<Column> columnList = new List<Column>();
        public Battery(int numberOfColumns, int totalNumberOfFloors, int numberOfBasements, int numberOfElevatorPerColumn)
        {
            
            // numFloors includes all the floors excluding the Ground Floor and the basements
            double numFloors = totalNumberOfFloors - numberOfBasements;
            int avgFloorPerColumn = (int)Math.Floor(numFloors / (numberOfColumns - 1));
            int fromFloor = 2;
            int toFloor = avgFloorPerColumn;
            int currentColumnID = 1;
            while (currentColumnID <= numberOfColumns)
            {
                // instantiation of the 1st column for the basements
                if (currentColumnID == 1)
                {
                    Column column = new Column(1, -numberOfBasements, - 1, numberOfElevatorPerColumn);
                    this.columnList.Add(column);
                }
                // instantiation of the other columns
                else if(currentColumnID < numberOfColumns)
                {
                    Column column = new Column(currentColumnID, fromFloor, toFloor, numberOfElevatorPerColumn);
                    this.columnList.Add(column);
                    fromFloor = toFloor + 1;
                    toFloor = toFloor + avgFloorPerColumn;
                }
                else
                {
                    Column column = new Column(currentColumnID, fromFloor, (int)numFloors, numberOfElevatorPerColumn);
                    this.columnList.Add(column);
                }
                currentColumnID = currentColumnID + 1;
            }
            // foreach (var item in columnList)
            // {
            //     // Console.WriteLine(" column {0}, numbre of elevator: {1}, floorLists: from {2} to {3}", item.ID, item.elevatorList.Count, item.floorList[0], item.floorList.Last());
            // }   
        }
        
        public void RequestElevator(int FloorNumbre)
        {
            Column currentColumn = this.columnList[0];
            // Finding the proper column
            foreach(var item in this.columnList)
            {
                if ( FloorNumbre >= item.floorList[1] && FloorNumbre <= item.floorList.Last()) 
                {
                    currentColumn = item;
                    break;
                }
            }

            // determining the USER Direction
            string Direction;
            if (FloorNumbre < 1)
            {
                Direction = "UP";
            }
            else 
            {
                Direction = "DOWN";
            }
            Console.WriteLine("Serving culomn:  columnID {0} from floor {1} to floor {2}", currentColumn.ID, currentColumn.floorList[1], currentColumn.floorList.Last());
            // Finding the best elevator based on comparing DistanceToGo
            int DistanceToGo = 1000;
            int distance;
            List<Elevator> FirstPriority = new List<Elevator>();
            List<Elevator> SecondPriority = new List<Elevator>();
            List<Elevator> ThirdPriority = new List<Elevator>();
            
            Elevator BestElevator = currentColumn.elevatorList[0];
            // finding the closest elevator Based on the following Priority: 
            //      1- the moving elevator which is arriving to the user
            //      2- the IDLE elevator
            //      3- other elevators
            foreach(Elevator elev in currentColumn.elevatorList)
            {   
                int currentDestination;
                if (elev.Direction == "IDLE")
                {
                    currentDestination = 0;
                }
                else
                {
                    currentDestination = elev.StopList.Last();
                }
                Console.Write("111elID = {0}, elPos = {1}, elDir = {2}, current Destination = {3}", elev.ID, elev.Position, elev.Direction, currentDestination);
                distance = CalculateDistanceToGo(elev, FloorNumbre, Direction);
                Console.WriteLine(". distanceToGo: {0}", distance);  
                if (elev.Direction == Direction)
                {
                    if ((Direction == "UP" && elev.Position <= FloorNumbre) | (Direction == "DOWN" && elev.Position >= FloorNumbre))
                    {
                        FirstPriority.Add(elev);
                    }
                }
                else if (elev.Direction == "IDLE") 
                {
                    SecondPriority.Add(elev);
                }
                else
                {
                    ThirdPriority.Add(elev);
                }
            }
            if (FirstPriority.Count > 0)
            {
                foreach (Elevator elev in FirstPriority)
                {
                    distance = CalculateDistanceToGo(elev, FloorNumbre, Direction);
                    // Console.WriteLine("#1elevator ID: {0} => DistanceToGo = {1}", elev.ID, distance);           
                    if ( distance <= DistanceToGo)
                    {
                        DistanceToGo = distance;
                        BestElevator = elev;
                    }
                }   
            }
            else if (SecondPriority.Count > 0)
            {
                foreach (Elevator elev in SecondPriority)
                {
                    distance = CalculateDistanceToGo(elev, FloorNumbre, Direction);
                    // Console.WriteLine("#2elevator ID: {0} => DistanceToGo = {1}", elev.ID, distance);           
                    if ( distance <= DistanceToGo)
                    {
                        DistanceToGo = distance;
                        BestElevator = elev;
                    }
                }
            }
            else
            {
                foreach (Elevator elev in ThirdPriority)
                {
                    distance = CalculateDistanceToGo(elev, FloorNumbre, Direction);
                    // Console.WriteLine("#3elevator ID: {0} => DistanceToGo = {1}", elev.ID, distance);           
                    if ( distance <= DistanceToGo)
                    {
                        DistanceToGo = distance;
                        BestElevator = elev;
                    }
                }
            }
            // Console.WriteLine("BEST ELEVATOR is ID: {0}", BestElevator.ID);
            // Updating the STOPLIST of the selected elevator
            if (BestElevator.Direction == Direction | BestElevator.Direction == "IDLE")
            {
                if (BestElevator.Direction == "DOWN" && BestElevator.Position >= FloorNumbre)
                {
                    Console.Write("%1 Take column {0} ElevatorID: {1} which is currently at floor {2}. ", currentColumn.ID, BestElevator.ID, BestElevator.Position);
                    UpdateList(BestElevator, BestElevator.StopList, FloorNumbre);
                    UpdateList(BestElevator, BestElevator.StopList, 1);
                    Console.WriteLine(" StopList: [ " + string.Join(" | ", BestElevator.StopList) + " ]");
                    // Console.WriteLine("*** 1%Take the column {0}, elevator {1} *** ", currentColumn.ID, BestElevator.ID);
                    move(BestElevator);
                }
                else if (BestElevator.Direction == "UP" && BestElevator.Position <= FloorNumbre)
                {
                    Console.Write("%2 Take column {0} ElevatorID: {1} which is currently at floor {2}. ", currentColumn.ID, BestElevator.ID, BestElevator.Position);
                    UpdateList(BestElevator, BestElevator.StopList, FloorNumbre);
                    UpdateList(BestElevator, BestElevator.StopList, 1);
                    Console.WriteLine(" StopList: [ " + string.Join(" | ", BestElevator.StopList) + " ]");
                    // Console.WriteLine("*** 2%Take the column {0}, elevator {1} *** ", currentColumn.ID, BestElevator.ID);
                    move(BestElevator);
                }
                else if (BestElevator.Direction == "IDLE")
                {
                    Console.Write("%3 Take ElevatorID: {0} which is currently at floor {1}. ", BestElevator.ID, BestElevator.Position);
                    UpdateList(BestElevator, BestElevator.StopList, FloorNumbre);
                    UpdateList(BestElevator, BestElevator.StopList, 1);
                    Console.WriteLine(" StopList: [ " + string.Join(" | ", BestElevator.StopList) + " ]");
                    // Console.WriteLine("*** 2%Take the column {0}, elevator {1} *** ", currentColumn.ID, BestElevator.ID);
                    move(BestElevator);
                }
                else
                {
                    Console.Write("%4 Take ElevatorID: {0} which is currently at floor {1}. ", BestElevator.ID, BestElevator.Position);
                    UpdateList(BestElevator, BestElevator.BufferList, FloorNumbre);
                    UpdateList(BestElevator, BestElevator.BufferList, 1);
                    Console.Write(" StopList: [ " + string.Join(" | ", BestElevator.StopList) + " ]");
                    Console.WriteLine(" BufferLsit: [ " + string.Join(" | ", BestElevator.BufferList) + " ]");
                    // Console.WriteLine("*** 3%Take the column {0}, elevator {1} *** ", currentColumn.ID, BestElevator.ID);
                    if (FloorNumbre > 1)
                    {
                        BestElevator.BufferDirection = "DOWN";
                        move(BestElevator);
                    }
                    else
                    {
                        BestElevator.BufferDirection = "UP";
                        move(BestElevator);
                    }
                }
            // Updating the BUFFERLIST t of the selected elevator
            }
            else
            {
                Console.Write("%5 Take ElevatorID: {0} which is currently at floor {1}. ", BestElevator.ID, BestElevator.Position);
                UpdateList(BestElevator, BestElevator.BufferList, FloorNumbre);
                UpdateList(BestElevator, BestElevator.StopList, 1);
                Console.Write(" StopList: [ " + string.Join(" | ", BestElevator.StopList) + " ]");
                Console.WriteLine(" BufferLsit: [ " + string.Join(" | ", BestElevator.BufferList) + " ]");

                // Console.WriteLine("*** 4%Take the column {0}, elevator {1} *** ", currentColumn.ID, BestElevator.ID);
                // For Basements
                if (FloorNumbre > 1)
                {
                    BestElevator.BufferDirection = "DOWN";
                    move(BestElevator);
                }
                // For other floors
                else
                {
                    BestElevator.BufferDirection = "UP";
                    move(BestElevator);
                }
            }
        }

        public void AssignElevator(int RequestedFloor)
        {
            // Finding the proper column
            Column currentColumn = this.columnList[0];
            foreach(var item in this.columnList)
            {
                // Console.WriteLine("current columnID {0} from floor {1} to floor {2}", item.ID, item.floorList[1], item.floorList.Last());
                if ( RequestedFloor >= item.floorList[1] && RequestedFloor <= item.floorList.Last()) 
                {
                    currentColumn = item;
                    break;
                }
            }
           Console.WriteLine("the column ID for floor {0} is {1}", RequestedFloor, currentColumn.ID);
           int DistanceToGo = 1000;
           Elevator BestElevator = currentColumn.elevatorList[0];
           string UserDirection;
           if (RequestedFloor > 1)
           {
               UserDirection = "UP";
           }
           else
           {
               UserDirection = "DOWN";
           }
           // Finding the best elevator based on comparing DistanceToGo
           foreach(Elevator elevator in currentColumn.elevatorList)
           {    
                int currentDestination;
                if (elevator.Direction == "IDLE")
                {
                    currentDestination = 0;
                }
                else
                {
                    currentDestination = elevator.StopList.Last();
                }
                Console.Write("111elID = {0}, elPos = {1}, elDir = {2}, current Destination = {3}", elevator.ID, elevator.Position, elevator.Direction, currentDestination);
                // Console.Write("elevatorID = {0}, Pos. = {1}, Dir. = {2}, current Destination = {3}", elevator.ID, elevator.Position, elevator.Direction, elevator.StopList.Last());
                int distance = CalculateDistanceToGo(elevator, 1, UserDirection);
                Console.WriteLine(". distanceToGo: {0}", distance);  
                // Console.WriteLine("elevator ID: {0} => DistanceToGo = {1}", elevator.ID, distance);           
                if ( distance <= DistanceToGo)
                {
                    DistanceToGo = distance;
                    BestElevator = elevator;
                }
           }
           Console.WriteLine("*** Take the column {0}, elevator {1} *** ", currentColumn.ID, BestElevator.ID);
           if (BestElevator.Position == 1)
           {
                // Console.WriteLine("%5ElevatorID: {0}", BestElevator.ID);
                UpdateList(BestElevator, BestElevator.StopList, RequestedFloor);    
           }
           else
           {
                // Console.Write("%6ElevatorID: {0}", BestElevator.ID);
                UpdateList(BestElevator, BestElevator.BufferList, RequestedFloor);
                // For Basements
                if (RequestedFloor > 1)
                {
                    BestElevator.BufferDirection = "DOWN";
                }
                // For other floors
                else
                {
                    BestElevator.BufferDirection = "UP";
                }
           }
           move(BestElevator);
           
           
        }
        public int CalculateDistanceToGo(Elevator elevator, int UserPosition, string UserDirection)
        {
            if (elevator.Direction != "IDLE" | elevator.StopList.Count != 0)
            {
                if (elevator.Direction == UserDirection)
                {
                    if (elevator.Direction == "UP" && elevator.Position <= UserPosition) 
                    {
                        return Math.Abs(elevator.Position - UserPosition);
                    }
                    else if (elevator.Direction == "DOWN" && elevator.Position >= UserPosition)
                    {
                        return Math.Abs(elevator.Position - UserPosition);
                    }
                    else
                    {
                        return Math.Abs(elevator.StopList.Last() - elevator.Position) + Math.Abs(elevator.StopList.Last() - UserPosition);    
                    }
                }
                else
                {
                    return Math.Abs(elevator.StopList.Last() - elevator.Position) + Math.Abs(elevator.StopList.Last() - UserPosition);;    
                }
            }
            else 
            {
                return Math.Abs(elevator.Position - UserPosition);
            }
        }
        public void UpdateList (Elevator elevator, List<int> List, int Position)
        {
            bool check = true;
            foreach(int stop in List)
            {
                if (stop == Position)
                {
                    check = false;
                }
            }
            if (check)
            {
                List.Add(Position);
                List.Sort();
            }
        }
        public void move(Elevator elevator)
        {
            while (elevator.StopList.Count > 0)
            {
                if (elevator.StopList[0] > elevator.Position)
                {
                    elevator.Direction = "UP";
                    while (elevator.Position < elevator.StopList[0])
                    {
                        elevator.Position += 1;
                        if (elevator.Position != 0)
                        {
                            Console.WriteLine("Elevator {0} is at floor {1} ", elevator.ID, elevator.Position);
                        }
                        if (elevator.Position == elevator.floorList.Last())
                        {
                            elevator.Direction = "IDLE";
                        }
                    }
                    elevator.Door = "OPEN";
                    Console.WriteLine("Door is open");
                    elevator.StopList.RemoveAt(0);
                }
                else 
                {
                    elevator.Direction = "DOWN";
                    while (elevator.Position > elevator.StopList.Last())
                    {
                        elevator.Position -= 1;
                        if (elevator.Position != 0)
                        {
                            Console.WriteLine("Elevator {0} is at floor {1} ", elevator.ID, elevator.Position);
                        }
                        if (elevator.Position == elevator.floorList.First())
                        {
                            elevator.Direction = "IDLE";
                        }
                    }
                    elevator.Door = "OPEN";
                    Console.WriteLine("Door is open");
                    elevator.StopList.RemoveAt(elevator.StopList.Count -1);
                }
                
                elevator.Door = "CLOSED";
                Console.WriteLine("Door is closed");
                elevator.Direction = "IDLE";
            }
            if (elevator.BufferList.Count > 0)
            {
                elevator.StopList = elevator.BufferList;
                elevator.Direction = elevator.BufferDirection;
                move(elevator);
            }
            else 
            {
                elevator.Direction = "IDLE";
            }
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            // Scenario 1
            void Scenario1 ()
            {
                Console.WriteLine("******************* ******************* *******************");
                Console.WriteLine("*******************      Scenario 1     *******************");
                Console.WriteLine("******************* ******************* *******************");
                Battery Battery1 = new Battery(4, 66, 6, 5);
                // Initializing Elevator 1 of Column 2
                Battery1.columnList[1].elevatorList[0].Position = 20;
                Battery1.columnList[1].elevatorList[0].Direction = "DOWN";
                Battery1.columnList[1].elevatorList[0].StopList.Add(5);
                // Initializing Elevator 2 of Column 2
                Battery1.columnList[1].elevatorList[1].Position = 2;
                Battery1.columnList[1].elevatorList[1].Direction = "UP";
                Battery1.columnList[1].elevatorList[1].StopList.Add(15);
                // // Initializing Elevator 3 of Column 2
                Battery1.columnList[1].elevatorList[2].Position = 13;
                Battery1.columnList[1].elevatorList[2].Direction = "DOWN";
                Battery1.columnList[1].elevatorList[2].StopList.Add(1);
                // // Initializing Elevator 4 of Column 2
                Battery1.columnList[1].elevatorList[3].Position = 15;
                Battery1.columnList[1].elevatorList[3].Direction = "DOWN";
                Battery1.columnList[1].elevatorList[3].StopList.Add(2);
                // // Initializing Elevator 5 of Column 2
                Battery1.columnList[1].elevatorList[4].Position = 6;
                Battery1.columnList[1].elevatorList[4].Direction = "DOWN";
                Battery1.columnList[1].elevatorList[4].StopList.Add(1);
                Console.WriteLine("******************* ******************* *******************");
                Console.WriteLine("******** User at floor 1. He goes UP to floor 20 ********");
                Console.WriteLine("*********** Elevator 5 from Column 2 is expected **********");
                Console.WriteLine("******************* ******************* *******************");
                Battery1.AssignElevator(20);
                
            }
            // Scenario 2
            void Scenario2 ()
            {
                Console.WriteLine("******************* ******************* *******************");
                Console.WriteLine("*******************      Scenario 2     *******************");
                Console.WriteLine("******************* ******************* *******************");
                Battery Battery2 = new Battery(4, 66, 6, 5);
                // Initializing Elevator 1 of Column 3
                Battery2.columnList[2].elevatorList[0].Position = 1;
                Battery2.columnList[2].elevatorList[0].Direction = "UP";
                Battery2.columnList[2].elevatorList[0].StopList.Add(21);
                // Initializing Elevator 2 of Column 3
                Battery2.columnList[2].elevatorList[1].Position = 23;
                Battery2.columnList[2].elevatorList[1].Direction = "UP";
                Battery2.columnList[2].elevatorList[1].StopList.Add(28);
                // // Initializing Elevator 3 of Column 3
                Battery2.columnList[2].elevatorList[2].Position = 33;
                Battery2.columnList[2].elevatorList[2].Direction = "DOWN";
                Battery2.columnList[2].elevatorList[2].StopList.Add(1);
                // // Initializing Elevator 4 of Column 3
                Battery2.columnList[2].elevatorList[3].Position = 40;
                Battery2.columnList[2].elevatorList[3].Direction = "DOWN";
                Battery2.columnList[2].elevatorList[3].StopList.Add(24);
                // // Initializing Elevator 5 of Column 3
                Battery2.columnList[2].elevatorList[4].Position = 39;
                Battery2.columnList[2].elevatorList[4].Direction = "DOWN";
                Battery2.columnList[2].elevatorList[4].StopList.Add(1);
                Console.WriteLine("******************* ******************* *******************");
                Console.WriteLine("******** User at floor 1. He goes UP to floor 36 ********");
                Console.WriteLine("*********** Elevator 1 from Column 3 is expected **********");
                Console.WriteLine("******************* ******************* *******************");
                Battery2.AssignElevator(36);
                
            }
            // Scenario 3
            void Scenario3 ()
            {
                Console.WriteLine("******************* ******************* *******************");
                Console.WriteLine("*******************      Scenario 3     *******************");
                Console.WriteLine("******************* ******************* *******************");
                Battery Battery3 = new Battery(4, 66, 6, 5);
                // Initializing Elevator 1 of Column 3
                Battery3.columnList[3].elevatorList[0].Position = 58;
                Battery3.columnList[3].elevatorList[0].Direction = "DOWN";
                Battery3.columnList[3].elevatorList[0].StopList.Add(1);
                // Initializing Elevator 2 of Column 3
                Battery3.columnList[3].elevatorList[1].Position =50;
                Battery3.columnList[3].elevatorList[1].Direction = "UP";
                Battery3.columnList[3].elevatorList[1].StopList.Add(60);
                // // Initializing Elevator 3 of Column 3
                Battery3.columnList[3].elevatorList[2].Position = 46;
                Battery3.columnList[3].elevatorList[2].Direction = "UP";
                Battery3.columnList[3].elevatorList[2].StopList.Add(58);
                // // Initializing Elevator 4 of Column 3
                Battery3.columnList[3].elevatorList[3].Position = 1;
                Battery3.columnList[3].elevatorList[3].Direction = "UP";
                Battery3.columnList[3].elevatorList[3].StopList.Add(54);
                // // Initializing Elevator 5 of Column 3
                Battery3.columnList[3].elevatorList[4].Position = 60;
                Battery3.columnList[3].elevatorList[4].Direction = "DOWN";
                Battery3.columnList[3].elevatorList[4].StopList.Add(1);
                // Battery3.AssignElevator();
                Console.WriteLine("******************* ******************* *******************");   
                Console.WriteLine("******** User at floor 54. He goes DOWN to floor 1 ********");
                Console.WriteLine("*********** Elevator 1 from Column 4 is expected **********");
                Console.WriteLine("******************* ******************* *******************");
                Battery3.RequestElevator(54);

                
            }
             // Scenario 4
            void Scenario4 ()
            {
                Console.WriteLine("******************* ******************* *******************");
                Console.WriteLine("*******************      Scenario 4     *******************");
                Console.WriteLine("******************* ******************* *******************");
                Battery Battery4 = new Battery(4, 66, 6, 5);
                // Initializing Elevator 1 of Column 4
                Battery4.columnList[0].elevatorList[0].Position = -4;
                Battery4.columnList[0].elevatorList[0].Direction = "IDLE";
                // Battery4.columnList[0].elevatorList[0].StopList.Add(1);
                // Initializing Elevator 2 of Column 4
                Battery4.columnList[0].elevatorList[1].Position = 1;
                Battery4.columnList[0].elevatorList[1].Direction = "IDLE";
                // Battery4.columnList[0].elevatorList[1].StopList.Add();
                // // Initializing Elevator 3 of Column 4
                Battery4.columnList[0].elevatorList[2].Position = -3;
                Battery4.columnList[0].elevatorList[2].Direction = "DOWN";
                Battery4.columnList[0].elevatorList[2].StopList.Add(-5);
                // // Initializing Elevator 4 of Column 4
                Battery4.columnList[0].elevatorList[3].Position = -6;
                Battery4.columnList[0].elevatorList[3].Direction = "UP";
                Battery4.columnList[0].elevatorList[3].StopList.Add(1);
                // // Initializing Elevator 5 of Column 4
                Battery4.columnList[0].elevatorList[4].Position = -1;
                Battery4.columnList[0].elevatorList[4].Direction = "DOWN";
                Battery4.columnList[0].elevatorList[4].StopList.Add(-6);
                // Battery3.AssignElevator();
                Console.WriteLine("******************* ******************* *******************");
                Console.WriteLine("********* User at floor -3. He goes UP to floor 1 *********");
                Console.WriteLine("*********** Elevator 4 from Column 1 is expected **********");
                Console.WriteLine("******************* ******************* *******************");
                Battery4.RequestElevator(-3);
            }
            Scenario1();
            Scenario2();
            Scenario3();
            Scenario4();
            // Console.ReadKey();

        }
    }
}
