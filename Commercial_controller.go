package main

import (
	"fmt"
	"math"
	"sort"
)

func main() {
	// Scenario1()
	Scenario2()
	Scenario3()
	Scenario4()
}

type CallButton struct {
	Direction string
	Floor     int
	Light     string
}
type Elevator struct {
	ID              int
	Position        int
	Direction       string
	StopList        []int
	FloorList       []int
	Door            string
	BufferDirection string
	BufferList      []int
}
type Column struct {
	ID           int
	ElevatorList []Elevator
	FloorList    []int
	CallButton   []CallButton
}
type Battery struct {
	ColumnList []Column
}

// Construction of a CallButton
func callButton(Direction string, Floor int) CallButton {
	m := new(CallButton)
	m.Direction = Direction
	m.Floor = Floor
	m.Light = "OFF"
	return *m
}

// Construction of an elevator
func elevator(ID, fromFloor, toFloor int) Elevator {
	m := new(Elevator)
	m.ID = ID
	for i := fromFloor; i <= toFloor; i++ {
		m.FloorList = append(m.FloorList, i)
	}
	return *m
}

// Construction of a column
func column(ID, fromFloor, toFloor, numberOfElevators int) Column {
	m := new(Column)
	m.ID = ID
	m.FloorList = append(m.FloorList, 1)
	// Creating Floor List for each Column
	for i := fromFloor; i <= toFloor; i++ {
		m.FloorList = append(m.FloorList, i)
	}
	// Creating Elevator List for each Column by creating new elevators,
	// knowing the range of floors for each column (fromFloor - toFloor)
	for i := 1; i <= numberOfElevators; i++ {
		m.ElevatorList = append(m.ElevatorList, elevator(i, fromFloor, toFloor))
	}
	// Creating CallButtons for Basements (at if clause) and then for floors (at else clause)
	// knowing the range of floors for each column (fromFloor - toFloor)
	if ID == 1 {
		for i := toFloor; i <= fromFloor; i++ {
			m.CallButton = append(m.CallButton, callButton("UP", i))
		}
	} else {
		for i := fromFloor; i <= toFloor; i++ {
			m.CallButton = append(m.CallButton, callButton("DOWN", i))
		}
	}
	fmt.Print("ColumnID ", ID, " supports these floors: ")
	for i := 0; i < len(m.FloorList); i++ {
		fmt.Printf("| %d ", m.FloorList[i])
	}
	fmt.Println("")

	return *m
}

// Construction of a battery
func battery(numberOfColumns, totalNumberOfFloors, numberOfBasements, numberOfElevatorsPerColumn int) Battery {
	m := new(Battery)
	numFloors := totalNumberOfFloors - numberOfBasements
	avgFloorPerColumn := int(math.Floor(float64(numFloors / (numberOfColumns - 1))))
	fromFloor := 2
	toFloor := avgFloorPerColumn
	currentColumnID := 1
	for currentColumnID <= numberOfColumns {
		// instantiation of the 1st column for the basements
		if currentColumnID == 1 {
			m.ColumnList = append(m.ColumnList, column(1, -numberOfBasements, -1, numberOfElevatorsPerColumn))
		} else if currentColumnID < numberOfColumns {
			// instantiation of the other columns
			m.ColumnList = append(m.ColumnList, column(currentColumnID, fromFloor, toFloor, numberOfElevatorsPerColumn))
			fromFloor = toFloor + 1
			toFloor = toFloor + avgFloorPerColumn
		} else {
			// instantiation of the last columns
			m.ColumnList = append(m.ColumnList, column(currentColumnID, fromFloor, numFloors, numberOfElevatorsPerColumn))
		}
		currentColumnID += 1
	}
	for i := 0; i < len(m.ColumnList); i++ {
		// fmt.Printf("Column %d   has %d elevators and sopports these floors: ", m.ColumnList[i].ID, len(m.ColumnList[i].ElevatorList))
		// for j := 0; j < len(m.ColumnList[i].FloorList); j++ {
		// 	fmt.Printf(" | %d", m.ColumnList[i].FloorList[j])
		// }
		// fmt.Println("")
	}

	return *m
}
func (c Battery) RequestElevator(FloorNumber int) {
	// Finding the proper column
	currentColumn := c.ColumnList[0]
	for i := 0; i < len(c.ColumnList); i++ {
		// fmt.Printf("floornumber = %d   and current column is %d \n", FloorNumber, i)
		// fmt.Printf("floornumber = %d   and current column is from %d  floor to %d floor\n", FloorNumber, c.ColumnList[i].FloorList[1], len(c.ColumnList[i].FloorList))
		if FloorNumber >= c.ColumnList[i].FloorList[1] && FloorNumber <= c.ColumnList[i].FloorList[len(c.ColumnList[i].FloorList)-1] {
			currentColumn = c.ColumnList[i]
		}
	}
	// determining the USER Direction
	var Direction string
	if FloorNumber < 1 {
		Direction = "UP"
	} else {
		Direction = "DOWN"
	}
	fmt.Printf("Serving culomn:  columnID %d from floor %d to floor %d \n", currentColumn.ID, currentColumn.FloorList[1], currentColumn.FloorList[len(currentColumn.FloorList)-1])
	// finding the closest elevator Based on on comparing DistanceToGo AND the following Priority:
	//      1- the moving elevator which is arriving to the user
	//      2- the IDLE elevator
	//      3- other elevators
	DistanceToGo := 1000
	var distance int
	var FirstPriority []Elevator
	var SecondPriority []Elevator
	var ThirdPriority []Elevator
	BestElevator := currentColumn.ElevatorList[0]
	var currentDestination int
	for i := 0; i < len(currentColumn.ElevatorList); i++ {
		elev := currentColumn.ElevatorList[i]
		if elev.Direction == "IDLE" {
			currentDestination = 0
		} else {
			currentDestination = elev.StopList[len(elev.StopList)-1]
		}
		fmt.Printf(" elevagtor ID = %d, Pos. = %d, Dir. = %s, current Destination = %d \n", elev.ID, elev.Position, elev.Direction, currentDestination)
		distance = c.CalculateDistanceToGo(elev, FloorNumber, Direction)
		// fmt.Printf("distanceToGo: %d \n", distance)
		if elev.Direction == Direction {
			if (Direction == "UP" && elev.Position <= FloorNumber) || (Direction == "DOWN" && elev.Position >= FloorNumber) {
				FirstPriority = append(FirstPriority, elev)
			}
		} else if elev.Direction == "IDLE" {
			SecondPriority = append(SecondPriority, elev)
		} else {
			ThirdPriority = append(ThirdPriority, elev)
		}
	}
	if len(FirstPriority) > 0 {
		for i := 0; i < len(FirstPriority); i++ {
			elev := FirstPriority[i]
			distance = c.CalculateDistanceToGo(elev, FloorNumber, Direction)
			// fmt.Println("#1elevator ID: {0} => DistanceToGo = {1}", elev.ID, distance)
			if distance <= DistanceToGo {
				DistanceToGo = distance
				BestElevator = elev
			}
		}
	} else if len(SecondPriority) > 0 {
		for i := 0; i < len(SecondPriority); i++ {
			elev := SecondPriority[i]
			distance = c.CalculateDistanceToGo(elev, FloorNumber, Direction)
			// Console.WriteLine("#2elevator ID: {0} => DistanceToGo = {1}", elev.ID, distance);
			if distance <= DistanceToGo {
				DistanceToGo = distance
				BestElevator = elev
			}
		}
	} else {
		for i := 0; i < len(ThirdPriority); i++ {
			elev := ThirdPriority[i]
			distance = c.CalculateDistanceToGo(elev, FloorNumber, Direction)
			// Console.WriteLine("#3elevator ID: {0} => DistanceToGo = {1}", elev.ID, distance);
			if distance <= DistanceToGo {
				DistanceToGo = distance
				BestElevator = elev
			}
		}
	}
	// Console.WriteLine("BEST ELEVATOR is ID: {0}", BestElevator.ID);
	// Updating the STOPList of the selected elevator
	if BestElevator.Direction == Direction || BestElevator.Direction == "IDLE" {
		if BestElevator.Direction == "DOWN" && BestElevator.Position >= FloorNumber {
			fmt.Printf("***111 Take column %d ElevatorID: %d which is currently at floor %d. \n ", currentColumn.ID, BestElevator.ID, BestElevator.Position)
			BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, FloorNumber)
			BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, 1)
			fmt.Println(" StopList: ")
			for i := 0; i < len(BestElevator.StopList); i++ {
				fmt.Print(" | ", BestElevator.StopList[i])
			}
			fmt.Println("")
			// fmt.PrintfLine(" StopList: [ " + string.Join(" | ", BestElevator.StopList) + " ]")
			// fmt.Printf("***1 Take the column %d, elevator %d *** \n", currentColumn.ID, BestElevator.ID)
			c.move(BestElevator)
		} else if BestElevator.Direction == "UP" && BestElevator.Position <= FloorNumber {
			fmt.Printf("***222 Take column %d ElevatorID: %d which is currently at floor %d. \n", currentColumn.ID, BestElevator.ID, BestElevator.Position)
			BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, FloorNumber)
			BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, 1)
			fmt.Print(" StopList: ")
			for i := 0; i < len(BestElevator.StopList); i++ {
				fmt.Print(" | ", BestElevator.StopList[i])
			}
			fmt.Println("")
			// fmt.Printf("***2 Take the column %d, elevator %d *** ", currentColumn.ID, BestElevator.ID)
			c.move(BestElevator)
		} else if BestElevator.Direction == "IDLE" {
			fmt.Printf("***333 Take ElevatorID: %d which is currently at floor %d. \n", BestElevator.ID, BestElevator.Position)
			BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, FloorNumber)
			BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, 1)
			fmt.Print(" StopList: ")
			for i := 0; i < len(BestElevator.StopList); i++ {
				fmt.Print(" | ", BestElevator.StopList[i])
			}
			fmt.Println("")
			// fmt.Printf("***3 Take the column %d, elevator %d *** ", currentColumn.ID, BestElevator.ID)
			c.move(BestElevator)
		}
		// Updating the BUFFERLIST t of the selected elevator
	} else {
		fmt.Printf("***444 Take ElevatorID: %d which is currently at floor %d. \n", BestElevator.ID, BestElevator.Position)
		BestElevator.BufferList = c.UpdateList(BestElevator, BestElevator.BufferList, FloorNumber)
		BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, 1)
		fmt.Print(" StopList: ")
		for i := 0; i < len(BestElevator.StopList); i++ {
			fmt.Print(" | ", BestElevator.StopList[i])
		}
		fmt.Println("")
		fmt.Print(" StopList: ")
		for i := 0; i < len(BestElevator.BufferList); i++ {
			fmt.Print(" | ", BestElevator.BufferList[i])
		}
		fmt.Println("")
		// fmt.Printf("***4 Take the column %d, elevator %d *** ", currentColumn.ID, BestElevator.ID)
		// For Basements
		if FloorNumber > 1 {
			BestElevator.BufferDirection = "DOWN"
			c.move(BestElevator)
			// For other floors
		} else {
			BestElevator.BufferDirection = "UP"
			c.move(BestElevator)
		}
	}
}
func (c Battery) AssignElevator(RequestedFloor int) {
	// Finding the proper column
	currentColumn := c.ColumnList[0]
	for i := 0; i < len(c.ColumnList); i++ {
		// fmt.Printf("floornumber = %d   and current column is %d \n", FloorNumber, i)
		// fmt.Printf("floornumber = %d   and current column is from %d  floor to %d floor\n", FloorNumber, c.ColumnList[i].FloorList[1], len(c.ColumnList[i].FloorList))
		if RequestedFloor >= c.ColumnList[i].FloorList[1] && RequestedFloor <= c.ColumnList[i].FloorList[len(c.ColumnList[i].FloorList)-1] {
			currentColumn = c.ColumnList[i]
		}
	}
	// determining the USER Direction
	var UserDirection string
	if RequestedFloor > 1 {
		UserDirection = "UP"
	} else {
		UserDirection = "DOWN"
	}
	fmt.Printf("Serving culomn:  columnID %d from floor %d to floor %d \n", currentColumn.ID, currentColumn.FloorList[1], currentColumn.FloorList[len(currentColumn.FloorList)-1])
	// Finding the best elevator based on comparing DistanceToGo
	DistanceToGo := 1000
	BestElevator := currentColumn.ElevatorList[0]
	for i := 0; i < len(currentColumn.ElevatorList); i++ {
		elevator := currentColumn.ElevatorList[i]
		var currentDestination int
		if elevator.Direction == "IDLE" {
			currentDestination = 0
		} else {
			currentDestination = elevator.StopList[len(elevator.StopList)-1]
		}
		fmt.Printf(" elevator ID = %d, Pos = %d, Dir = %s, current Destination = %d \n", elevator.ID, elevator.Position, elevator.Direction, currentDestination)
		distance := c.CalculateDistanceToGo(elevator, 1, UserDirection)
		// fmt.Println("distanceToGo: ", distance)
		if distance < DistanceToGo {
			DistanceToGo = distance
			BestElevator = elevator
		}
	}
	fmt.Printf("***666 Take the column %d, elevator %d  ***  \n", currentColumn.ID, BestElevator.ID)
	if BestElevator.Position == 1 {
		// fmt.Print("666 current stoplist BEFORE update: ")
		// for i := 0; i < len(BestElevator.StopList); i++ {
		// 	fmt.Print(" | ", BestElevator.StopList[i])
		// }
		// fmt.Println("")
		BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.StopList, RequestedFloor)
		// fmt.Print("666 current stoplist AFTER update: ")
		// for i := 0; i < len(BestElevator.StopList); i++ {
		// 	fmt.Print(" | ", BestElevator.StopList[i])
		// }
		// fmt.Println("")
	} else {
		// fmt.Print("666 current Bufferlist BEFORE update: ")
		// for i := 0; i < len(BestElevator.StopList); i++ {
		// 	fmt.Print(" | ", BestElevator.StopList[i])
		// }
		// fmt.Println("")
		BestElevator.StopList = c.UpdateList(BestElevator, BestElevator.BufferList, RequestedFloor)
		// fmt.Print("666 current Bufferlist BEFORE update: ")
		// for i := 0; i < len(BestElevator.StopList); i++ {
		// 	fmt.Print(" | ", BestElevator.StopList[i])
		// }
		// fmt.Println("")
		// Setting Buffer direction For Basements
		if RequestedFloor > 1 {
			BestElevator.BufferDirection = "DOWN"
			// Setting Buffer direction For other floors
		} else {
			BestElevator.BufferDirection = "UP"
		}
	}
	c.move(BestElevator)
}
func (c Battery) CalculateDistanceToGo(elevator Elevator, UserPosition int, UserDirection string) int {
	if elevator.Direction != "IDLE" || len(elevator.StopList) != 0 {
		if elevator.Direction == UserDirection {
			if elevator.Direction == "UP" && elevator.Position <= UserPosition {
				// fmt.Println("check1 user direction", UserDirection)
				return int(math.Abs(float64(elevator.Position - UserPosition)))
			} else if elevator.Direction == "DOWN" && elevator.Position >= UserPosition {
				// fmt.Println("check2 user direction", UserDirection)
				return int(math.Abs(float64(elevator.Position - UserPosition)))
			} else {
				// fmt.Println("check3 user direction", UserDirection)
				return int(math.Abs(float64(elevator.StopList[len(elevator.StopList)-1]-elevator.Position))) + int(math.Abs(float64(elevator.StopList[len(elevator.StopList)-1]-UserPosition)))
			}
		} else {
			// fmt.Println("check4 user direction", UserDirection)
			return int(math.Abs(float64(elevator.StopList[len(elevator.StopList)-1]-elevator.Position))) + int(math.Abs(float64(elevator.StopList[len(elevator.StopList)-1]-UserPosition)))
		}
	} else {
		// fmt.Println("check5 user direction", UserDirection)
		return int(math.Abs(float64(elevator.Position - UserPosition)))
	}
}
func (c Battery) UpdateList(elevator Elevator, List []int, Position int) []int {
	check := true
	for i := 0; i < len(List); i++ {
		stop := List[i]
		if stop == Position {
			check = false
		}
	}
	if check {
		List = append(List, Position)
		sort.Ints(List)
	}
	return List
}
func (c Battery) move(elevator Elevator) {
	i := 0
	for i <= len(elevator.StopList) {
		if elevator.StopList[0] > elevator.Position {
			elevator.Direction = "UP"
			j := elevator.Position
			for j < elevator.StopList[0] {
				elevator.Position += 1
				if elevator.Position != 0 {
					fmt.Printf("Elevator %d is at floor %d \n", elevator.ID, elevator.Position)
				}
				if elevator.Position == elevator.FloorList[len(elevator.FloorList)-1] {
					elevator.Direction = "IDLE"
				}
				j++
			}
			elevator.Door = "OPEN"
			fmt.Println("Door is open")
			// fmt.Print("111 current stoplist BEFORE remove: ")
			// for i := 0; i < len(elevator.StopList); i++ {
			// 	fmt.Print(" | ", elevator.StopList[i])
			// }
			// fmt.Println("")
			elevator.StopList = elevator.StopList[1:]
			// fmt.Print("111 current stoplist AFTER remove: ")
			// for i := 0; i < len(elevator.StopList); i++ {
			// 	fmt.Print(" | ", elevator.StopList[i])
			// }
			// fmt.Println("")
		} else {
			elevator.Direction = "DOWN"
			j := elevator.Position
			for j > elevator.StopList[len(elevator.StopList)-1] {
				elevator.Position -= 1
				if elevator.Position != 0 {
					fmt.Printf("Elevator %d is at floor %d \n", elevator.ID, elevator.Position)
				}
				if elevator.Position == elevator.FloorList[0] {
					elevator.Direction = "IDLE"
				}
				j--
			}
			elevator.Door = "OPEN"
			// fmt.Println("Door is open")
			// fmt.Print("222 current stoplist BEFORE remove: ")
			// for i := 0; i < len(elevator.StopList); i++ {
			// 	fmt.Print(" | ", elevator.StopList[i])
			// }
			// fmt.Println("")
			elevator.StopList = elevator.StopList[:len(elevator.StopList)-1]
			// fmt.Print("222 current stoplist AFTER remove: ")
			// for i := 0; i < len(elevator.StopList); i++ {
			// 	fmt.Print(" | ", elevator.StopList[i])
			// }
			// fmt.Println("")
		}
		i++
		elevator.Door = "CLOSED"
		fmt.Println("Door is closed")
		elevator.Direction = "IDLE"
	}
	if len(elevator.BufferList) > 0 {
		elevator.StopList = elevator.BufferList
		elevator.Direction = elevator.BufferDirection
		c.move(elevator)
	} else {
		elevator.Direction = "IDLE"
	}

}

// Scenario 1
func Scenario1() {
	fmt.Println("******************* ******************* *******************")
	fmt.Println("*******************      Scenario 1     *******************")
	fmt.Println("******************* ******************* *******************")
	Battery1 := battery(4, 66, 6, 5)
	// Initializing Elevator 1 of Column 2
	Battery1.ColumnList[1].ElevatorList[0].Position = 20
	Battery1.ColumnList[1].ElevatorList[0].Direction = "DOWN"
	Battery1.ColumnList[1].ElevatorList[0].StopList = append(Battery1.ColumnList[1].ElevatorList[0].StopList, 5)
	// Initializing Elevator 2 of Column 2
	Battery1.ColumnList[1].ElevatorList[1].Position = 2
	Battery1.ColumnList[1].ElevatorList[1].Direction = "UP"
	Battery1.ColumnList[1].ElevatorList[1].StopList = append(Battery1.ColumnList[1].ElevatorList[1].StopList, 15)
	// // Initializing Elevator 3 of Column 2
	Battery1.ColumnList[1].ElevatorList[2].Position = 13
	Battery1.ColumnList[1].ElevatorList[2].Direction = "DOWN"
	Battery1.ColumnList[1].ElevatorList[2].StopList = append(Battery1.ColumnList[1].ElevatorList[2].StopList, 1)
	// // Initializing Elevator 4 of Column 2
	Battery1.ColumnList[1].ElevatorList[3].Position = 15
	Battery1.ColumnList[1].ElevatorList[3].Direction = "DOWN"
	Battery1.ColumnList[1].ElevatorList[3].StopList = append(Battery1.ColumnList[1].ElevatorList[3].StopList, 2)
	// // Initializing Elevator 5 of Column 2
	Battery1.ColumnList[1].ElevatorList[4].Position = 6
	Battery1.ColumnList[1].ElevatorList[4].Direction = "DOWN"
	Battery1.ColumnList[1].ElevatorList[4].StopList = append(Battery1.ColumnList[1].ElevatorList[4].StopList, 1)
	fmt.Println("******************* ******************* *******************")
	fmt.Println("******** User at floor 1. He goes UP to floor 20 ********")
	fmt.Println("*********** Elevator 5 from Column 2 is expected **********")
	fmt.Println("******************* ******************* *******************")
	Battery1.AssignElevator(20)
}

// Scenario 2
func Scenario2() {
	fmt.Println("******************* ******************* *******************")
	fmt.Println("*******************      Scenario 2     *******************")
	fmt.Println("******************* ******************* *******************")
	Battery2 := battery(4, 66, 6, 5)
	// Initializing Elevator 1 of Column 3
	Battery2.ColumnList[2].ElevatorList[0].Position = 1
	Battery2.ColumnList[2].ElevatorList[0].Direction = "UP"
	Battery2.ColumnList[2].ElevatorList[0].StopList = append(Battery2.ColumnList[2].ElevatorList[0].StopList, 21)
	// Initializing Elevator 2 of Column 3
	Battery2.ColumnList[2].ElevatorList[1].Position = 23
	Battery2.ColumnList[2].ElevatorList[1].Direction = "UP"
	Battery2.ColumnList[2].ElevatorList[1].StopList = append(Battery2.ColumnList[2].ElevatorList[1].StopList, 28)
	// // Initializing Elevator 3 of Column 3
	Battery2.ColumnList[2].ElevatorList[2].Position = 33
	Battery2.ColumnList[2].ElevatorList[2].Direction = "DOWN"
	Battery2.ColumnList[2].ElevatorList[2].StopList = append(Battery2.ColumnList[2].ElevatorList[2].StopList, 1)
	// // Initializing Elevator 4 of Column 3
	Battery2.ColumnList[2].ElevatorList[3].Position = 40
	Battery2.ColumnList[2].ElevatorList[3].Direction = "DOWN"
	Battery2.ColumnList[2].ElevatorList[3].StopList = append(Battery2.ColumnList[2].ElevatorList[3].StopList, 24)
	// // Initializing Elevator 5 of Column 3
	Battery2.ColumnList[2].ElevatorList[4].Position = 39
	Battery2.ColumnList[2].ElevatorList[4].Direction = "DOWN"
	Battery2.ColumnList[2].ElevatorList[4].StopList = append(Battery2.ColumnList[2].ElevatorList[4].StopList, 1)
	fmt.Println("******************* ******************* *******************")
	fmt.Println("******** User at floor 1. He goes UP to floor 36 ********")
	fmt.Println("*********** Elevator 1 from Column 3 is expected **********")
	fmt.Println("******************* ******************* *******************")
	Battery2.AssignElevator(36)
}

// Scenario 3
func Scenario3() {
	fmt.Println("******************* ******************* *******************")
	fmt.Println("*******************      Scenario 3     *******************")
	fmt.Println("******************* ******************* *******************")
	Battery3 := battery(4, 66, 6, 5)
	// Initializing Elevator 1 of Column 3
	Battery3.ColumnList[3].ElevatorList[0].Position = 58
	Battery3.ColumnList[3].ElevatorList[0].Direction = "DOWN"
	Battery3.ColumnList[3].ElevatorList[0].StopList = append(Battery3.ColumnList[3].ElevatorList[0].StopList, 1)
	// Initializing Elevator 2 of Column 3
	Battery3.ColumnList[3].ElevatorList[1].Position = 50
	Battery3.ColumnList[3].ElevatorList[1].Direction = "UP"
	Battery3.ColumnList[3].ElevatorList[1].StopList = append(Battery3.ColumnList[3].ElevatorList[1].StopList, 60)
	// // Initializing Elevator 3 of Column 3
	Battery3.ColumnList[3].ElevatorList[2].Position = 46
	Battery3.ColumnList[3].ElevatorList[2].Direction = "UP"
	Battery3.ColumnList[3].ElevatorList[2].StopList = append(Battery3.ColumnList[3].ElevatorList[2].StopList, 58)
	// // Initializing Elevator 4 of Column 3
	Battery3.ColumnList[3].ElevatorList[3].Position = 1
	Battery3.ColumnList[3].ElevatorList[3].Direction = "UP"
	Battery3.ColumnList[3].ElevatorList[3].StopList = append(Battery3.ColumnList[3].ElevatorList[3].StopList, 54)
	// // Initializing Elevator 5 of Column 3
	Battery3.ColumnList[3].ElevatorList[4].Position = 60
	Battery3.ColumnList[3].ElevatorList[4].Direction = "DOWN"
	Battery3.ColumnList[3].ElevatorList[4].StopList = append(Battery3.ColumnList[3].ElevatorList[4].StopList, 1)
	// Battery3.AssignElevator();
	fmt.Println("******************* ******************* *******************")
	fmt.Println("******** User at floor 54. He goes DOWN to floor 1 ********")
	fmt.Println("*********** Elevator 1 from Column 4 is expected **********")
	fmt.Println("******************* ******************* *******************")
	Battery3.RequestElevator(54)
}

// Scenario 4
func Scenario4() {
	fmt.Println("******************* ******************* *******************")
	fmt.Println("*******************      Scenario 4     *******************")
	fmt.Println("******************* ******************* *******************")
	Battery4 := battery(4, 66, 6, 5)
	// Initializing Elevator 1 of Column 4
	Battery4.ColumnList[0].ElevatorList[0].Position = -4
	Battery4.ColumnList[0].ElevatorList[0].Direction = "IDLE"
	// Battery4.ColumnList[0].ElevatorList[0].StopList = append(Battery4.ColumnList[0].ElevatorList[0].StopList, 1)
	// Initializing Elevator 2 of Column 4
	Battery4.ColumnList[0].ElevatorList[1].Position = 1
	Battery4.ColumnList[0].ElevatorList[1].Direction = "IDLE"
	// Battery4.ColumnList[0].ElevatorList[1].StopList = append(Battery4.ColumnList[0].ElevatorList[1].StopList, );
	// // Initializing Elevator 3 of Column 4
	Battery4.ColumnList[0].ElevatorList[2].Position = -3
	Battery4.ColumnList[0].ElevatorList[2].Direction = "DOWN"
	Battery4.ColumnList[0].ElevatorList[2].StopList = append(Battery4.ColumnList[0].ElevatorList[2].StopList, -5)
	// // Initializing Elevator 4 of Column 4
	Battery4.ColumnList[0].ElevatorList[3].Position = -6
	Battery4.ColumnList[0].ElevatorList[3].Direction = "UP"
	Battery4.ColumnList[0].ElevatorList[3].StopList = append(Battery4.ColumnList[0].ElevatorList[3].StopList, 1)
	// // Initializing Elevator 5 of Column 4
	Battery4.ColumnList[0].ElevatorList[4].Position = -1
	Battery4.ColumnList[0].ElevatorList[4].Direction = "DOWN"
	Battery4.ColumnList[0].ElevatorList[4].StopList = append(Battery4.ColumnList[0].ElevatorList[4].StopList, -6)
	// Battery3.AssignElevator();
	fmt.Println("******************* ******************* *******************")
	fmt.Println("********* User at floor -3. He goes UP to floor 1 *********")
	fmt.Println("*********** Elevator 4 from Column 1 is expected **********")
	fmt.Println("******************* ******************* *******************")
	Battery4.RequestElevator(-3)
}
