from tkinter import *
import time
import random

#Coordiante System: (Left,Top,Right,Bottom)
floors_info = {}
elevators_info = {}




main_window = Tk()
main_window.title("Personal Control System Animation")

window_canvas = Canvas(main_window, width=1300, height=650, bg="orange")
window_canvas.pack()

"""This goes to every floor and increments the total people waiting
    at each floor to give a final total of how many people are waiting.
    This total is displayed on the UI and this function is ran
    everytime info_present() is called."""
def waiting_count(floor_amount):
    waiting_amount = 0
    for count in range(floor_amount):
        floor_people_amount = len(floors_info[count]["people_waiting"])
        waiting_amount += floor_people_amount
    return str(waiting_amount)


"""This loops through each floor and increments the total people
   that have been dropped off to an ongoing running totatl.
   This ongoing running is displayed on the UI and this function
   is ran everytime info_present() is called."""
def dropped_off_count(floor_amount):
    dropped_amount = 0
    for count in range(floor_amount):
        floor_people_amount = len(floors_info[count]["people_finished"])
        dropped_amount += floor_people_amount
    return str(dropped_amount)


"""This calculates the cost of the algorithm. When the function is
   called a loop is run throug floors_info and all of the people
   that are finished are looked at. Their waiting is accessed and
   incremented onto an ongoing total. This is then divided by the
   amount of people and the amount of lifts. This function is called
   everytime info_present is called."""
def person_time_calc(people_amount,  floor_amount, lifts_amount):
    person_time_sum = 0
    #Iterates through each dictionary
    for floor_num in range(floor_amount):
        floor_people = floors_info[floor_num]["people_finished"]
        #Increments person time sum
        for customer in floor_people:
            person_time_sum += customer[2]
    #Calculates Average
    person_time_average = (person_time_sum//(people_amount*lifts_amount))
    return str(person_time_average)
       
   

"""This displays information about the current status of the algorithm.
   Whenever this function is called, so is dropped_off_count(n),
   time_average(m,n,o) and waiting_count(n). A silver box displays the
   values returned from these functions. This enables the user to see
   how many people are waiting, how many people are dropped off and the
   current average waiting time for a person. This function is called
   everytime someone is picked up or dropped off."""
def info_present(people_amount, floor_amount, lifts_amount):
    people_waiting = waiting_count(floor_amount)
    people_dropped_off = dropped_off_count(floor_amount)
    time_average = person_time_calc(people_amount, floor_amount, lifts_amount)
    information_panel = Label(window_canvas, text = ("People Waiting: " +people_waiting+"\n" +
                                                    "People Dropped Off: " +people_dropped_off+"\n"+
                                                    "Average Time Taken: " +time_average))

    window_canvas.create_window(650, 50, window=information_panel)

"""This function helps calculate the cost of the algorithm. Firstly
   floors_info is iterated through where the people waiting is looked
   at. Each of their waiting times, is incremented. Then elevators_info
   is iterated through. Each person in the lift is looked in the lift.
   Each of their waiting times are incremented by 1. This function is
   called everytime an elevator reaches a floor."""
def person_time_increment(name, lift_names):
    #Increment Total For Waiting People
    for level_num in floors_info:
        for waiting_guy in floors_info[level_num]["people_waiting"]:
            waiting_guy[2] += 1
    #Increment Total For People In Lifts
    for each_name in lift_names:
        lift_guys = elevators_info[each_name]["people_there"]
        for guy in lift_guys:
            guy[2] += 1



"""This creates the sides of the buildings. Two lines are created
   use the create_line widget. """
def create_sides():
    left_side = window_canvas.create_line(200, 640, 200, 15,width=10,
                                   fill="blue")
    right_side = window_canvas.create_line(1100, 640, 1100, 15, width=10,
                                    fill="blue")
#create_sides()


"""This creates the floors in the building. The configured amount of
   floors entered by the user is passed through this function and loop
   is itereated dependent on the integer value passed as an argument.
   A floor is created on the UI using the create_line widget. Everytime
   a floor is created a dictionary is added to floors_info to represent this
   floor. This dictionary is a module variable and will be updated and
   changed throughout the program. Then the the position for the next floor
   is calculated using between_space. This is the space in between the floors
   which is calculated using the amount of floors configured by the user."""
def create_floors(floor_amount):
    between_space = (590//floor_amount)
    floor_position = 620
    ground_num = 0
    while floor_position != 30 and ground_num != floor_amount:
        #Creating floor on interface
        window_canvas.create_line(205, floor_position, 1095, floor_position, width=5)
        #Creating dictionary for each floor
        floors_info[ground_num] = {"graphic_position":floor_position,"waiting_mass":0,
                                   "people_waiting":[],"people_finished":[]}
        floor_position = floor_position - between_space
        ground_num += 1
        if floor_position < 30:
            break

#create_floors(10)

#840

        


"""This enables the lift in the opposite direction when the
   lift reaches the top floor or bottom floor. This enables
   the lifts to move continuosly picking people up and
   dropping them off. The position is passed through so
   the function can check if the position of a lift is
   at the top or bottom. Speed is passed through so the
   speed of the lift can be changed to the opposite of what
   it was, which means the lift will move in the opposite
   direction. This function is called everytime a lift
   reaches a floor."""
def speed_changer(position, speed):
    #Moves in opposite direction when lift reaches top
    #60
    if position <= 60:
        speed = -(speed)
    #Moves in opposite direction when lift reaches bottom
    #640
    elif position >= 640:
        speed = -(speed)
    return speed



"""This function runs everytime collection_evaluator
   runs. This takes a 2D list where each list contains
   the ID of the elevator and the remaining weight
   capacity. Based on the remaining weight capacity,
   the lists inside the list are sorted using the merge
   sort algorithm."""
def elevator_merge_sort(sorting_list):
    if len(sorting_list) > 1:
        division_point = len(sorting_list)//2
        left_side = sorting_list[:division_point]
        right_side = sorting_list[division_point:]
        elevator_merge_sort(left_side)
        elevator_merge_sort(right_side)
        i = 0
        j = 0
        k = 0
        while i < len(left_side) and j < len(right_side):
            if left_side[i][1] < right_side[j][1]:
                sorting_list[k] = left_side[i]
                i += 1
            else:
                sorting_list[k] = right_side[j]
                j += 1
            k += 1
        while i < len(left_side):
            sorting_list[k] = left_side[i]
            i += 1
            k += 1

        while j < len(right_side):
            sorting_list[k] = right_side[j]
            j += 1
            k += 1
    return sorting_list



"""This function is designed to calculate which is the best
   elevator for pickup in the instance where there are more
   than 1 lift that is stopped at a floor. The the function
   iterates through elevators_info and looks at the remaining
   capacity of all the elevators. It then stores each remaining
   capacity with the corresponding lift in a dictionary called
   lift_capacities. This is then sorted into an order from best
   to worst and then this order is appended to a list. This is
   then returned at the end of the function. This function is called
   whenever a pickup needs to be made."""
def collection_evaluator(lifts_at_floor):
    #lift_capacities = {}
    final_options = []
    array_for_sorting = []
    #Checking Capacity of all Lifts at Floor
    for lift in lifts_at_floor:
        if elevators_info[lift]["remaining_weight"] > 0:
            if len(elevators_info[lift]["people_there"]) < 10:
                array_space = []
                array_space.append(lift)
                array_space.append(elevators_info[lift]["remaining_weight"])
                array_for_sorting.append(array_space)
    if len(array_for_sorting) == 0:
        return []
    else:
        #Sorting Array
        sorted_lifts = reversed(elevator_merge_sort(array_for_sorting))
        #sorted_lifts = sorted(lift_capacities.items(), key=lambda x: x[1])
        #Creating list of lifts in order of capacity
        final_options = []
        for each_capacity in sorted_lifts:
            final_options.append(each_capacity[0])
        return final_options



"""This function checks the remaining capacity of each
   elevator. If there is no capacity in the elevator the
   elevator on the UI becomes red instead of green. Otherwise
   the colour stays green. """        
def full_capacity_checker(name):
    if (elevators_info[name]["remaining_weight"] <= 0 or
        len(elevators_info[name]["people_there"]) >= 10):
            window_canvas.itemconfig(name, fill="red")
    else:
        window_canvas.itemconfig(name, fill="green")

"""This function assigns the elevator an initial target.
   This is so when the elevators are starting at the ground
   floor, they can split up onto individual floors. This
   function enables them to split onto different floors."""
def new_target_assignment(lifts_amount, floor_amount, each_lift,
                          initial_speed, lift_names):
    current_target = elevators_info[each_lift]["target_floor"]
    if initial_speed < 0:
        new_target = current_target + lifts_amount
        if new_target > (floor_amount-1):
            new_target = (floor_amount-1) - (lift_names.index(each_lift) + 1)
    if initial_speed > 0:
        new_target = current_target - lifts_amount
        if new_target < 0:
            new_target = 0 + (lift_names.index(each_lift) + 1)

    return new_target




"""This redefines the lowest floor that each elevator
   elevator has to go to. It first finds the lowest floor
   where someone needs to be picked up from and then
   the lowest floor where someone needs to be dropped off
   to. These results are compared and the lower of the two
   is considered as the lowest point an elevator needs to
   go to."""
def lowest_floor_decider(floor_amount):
    #Finding Lowest Floor for Pickup
    for level in floors_info:
        level_people = floors_info[level]["people_waiting"]
        if len(level_people) != 0:
            lowest_pickup_point = level
            break
        else:
            lowest_pickup_point = (floor_amount-1)

    #Finding Lowest Floor for Dropoff
    lowest_dropping_points = []
    for elevator_num in elevators_info:
        elevator_destinations = elevators_info[elevator_num]["destinations"]
        if elevator_destinations != []:
            lowest_dropping_points.append(min(elevator_destinations))
    if lowest_dropping_points != []:
        lowest_dropoff_point = min(lowest_dropping_points)
    else:
        lowest_dropoff_point = (floor_amount-1)

    #Finding Overall Lowest Floor
    if lowest_pickup_point == (floor_amount-1) and lowest_dropoff_point == (floor_amount-1):
        lowest_floor = 0
    elif lowest_pickup_point < lowest_dropoff_point:
        lowest_floor = lowest_pickup_point
    elif lowest_dropoff_point < lowest_pickup_point:
        lowest_floor = lowest_dropoff_point
    elif lowest_dropoff_point == lowest_pickup_point:
        lowest_floor = lowest_dropoff_point

    return lowest_floor


"""This redefines the highest floor that each elevator
   has to go to. It first finds the highest floor
   where someone nees to be picked up from and then
   the highest floor where someone needs to be dropped off
   to. These results are compared and the higher of the two
   is considered as the highest point an elevator needs to go
   to."""
def highest_floor_decider(floor_amount):
    #Finding Highest Floor for Pickup
    level = (floor_amount-1)
    for level in reversed(floors_info):
        level_people = floors_info[level]["people_waiting"]
        if len(level_people) != 0:
            highest_pickup_point = level
            break
        else:
            highest_pickup_point = 0
        level = level - 1

    #Finding Highest Floor for Dropoff
    highest_dropping_points = []
    for elevator_num in elevators_info:
        elevator_destinations = elevators_info[elevator_num]["destinations"]
        if elevator_destinations != []:
            highest_dropping_points.append(max(elevator_destinations))
    if highest_dropping_points != []:
        highest_dropoff_point = max(highest_dropping_points)
    else:
        highest_dropoff_point = 0


    #Finding Overall Highest Floor
    if highest_dropoff_point == 0 and highest_pickup_point == 0:
        highest_floor = floor_amount-1
    elif highest_dropoff_point > highest_pickup_point:
        highest_floor = highest_dropoff_point
    elif highest_pickup_point > highest_dropoff_point:
        highest_floor = highest_pickup_point
    elif highest_pickup_point == highest_dropoff_point:
        highest_floor = highest_pickup_point

    return highest_floor
    

"""At every floor this function is ran to see which elevators
   are at the floor. The ID's of these lifts are appended to
   a list that are returned at the end of the function. This
   function is ran in create_multiple_elevators."""
def lift_finder(floor_amount, lift_names, floor_position, elevator_speed):
    floor_lifts = []
    for name in lift_names:
        #Compares position of lift against postion of floor that is being
        #currently checked
        lift_position = elevators_info[name]["graphic_position"]
        if floor_position == lift_position:
            floor_lifts.append(name)
            person_time_increment(name, lift_names)


    return floor_lifts



"""This is function runs most of th simulation. Firstly the elevator
   are created in their respective positions. This is complicated as
   you have to have the elevators spaced out evenly and all on the
   bottom floor. Then for each elevator a dictionary is created, to
   represent the elevator. The elevators then all travel to their
   inital floor targets and stop there. They do necessary pickups and
   dropoffs and then all the elevators start travelling at once, one
   floor at a time. This is done until everyone is dropped off. During
   this process functions are run for people to be picked up, dropped off,
   and the highest and lowest points the elevators travel to are
   redefined. Functions are also executed to alert which elevators have
   reached their maximum capacity."""
def create_multiple_elevators(people_amount, floor_amount, lifts_amount):
    #Creating Lifts
    between_space = 900//lifts_amount
    heights = {"first_kind": (630, 650),
               "second_kind": (40, 60)}
    lift_names = []
    #Assigning ID's for each lift
    for num in range(65, (65+lifts_amount)):
        lift_names.append(chr(num))
    for each_lift in range(lifts_amount):
        lift_name = lift_names[each_lift]
        #Creating dictionary for each lift
        elevators_info[lift_name] = {"graphic_position":0, "lift_speed":0,
                                     "remaining_weight":1200,
                                     "people_there":[], "destinations":[],
                                     "target_floor":0}
    starting_position = 210
    for every_lift in range(lifts_amount):
        #Creating lifts on interface
        window_canvas.create_rectangle(starting_position, heights["first_kind"][0],
                                      (starting_position+20), heights["first_kind"][1],
                                      fill="green", tags = lift_names[every_lift])
        starting_position += between_space

    #Initial Motion

    #Floor Target Assignments
    for floor_target in range(lifts_amount):
        elevators_info[lift_names[floor_target]]["target_floor"] = floor_target

    #Travelling to Floor Targets
    for seperate_lift in lift_names:
        elevator_speed = -0.1
        elevators_info[seperate_lift]["lift_speed"] = elevator_speed
        position_of_lift = int(window_canvas.coords(seperate_lift)[1])
        lift_target = elevators_info[seperate_lift]["target_floor"]
        target_position = floors_info[lift_target]["graphic_position"]
        while position_of_lift != target_position:
            window_canvas.move(seperate_lift, 0, elevators_info[seperate_lift]["lift_speed"])
            position_of_lift = int(window_canvas.coords(seperate_lift)[1])
            elevators_info[seperate_lift]["graphic_position"] = position_of_lift
            #Stopping the elevator at the target floor
            if position_of_lift == target_position:
                elevators_info[seperate_lift]["lift_speed"] = 0
                waiting_amount = len(floors_info[lift_target]["people_waiting"])
                if waiting_amount > 0:
                    #Picking people up
                    people_collection(floor_amount, lift_target, elevator_speed, seperate_lift)
                    info_present(people_amount, floor_amount, lifts_amount)
                    full_capacity_checker(seperate_lift)

            main_window.update()
        elevators_info[seperate_lift]["target_floor"] += lifts_amount

    #Rest Of Motion
    #-0.8
    elevator_speed = -0.8
    #Initialising Lift Speeds
    for lift in lift_names:
        elevators_info[lift]["lift_speed"] = elevator_speed

    #Rest of Motion Completion
    finished_amount = 0
    while finished_amount != people_amount:
        for each_lift in lift_names:
            window_canvas.move(each_lift, 0, elevators_info[each_lift]["lift_speed"])
            position_of_lift = int(window_canvas.coords(each_lift)[1])
            elevators_info[each_lift]["graphic_position"] = position_of_lift
            elevators_info[each_lift]["lift_speed"] = speed_changer(elevators_info[each_lift]["graphic_position"],
                                                                    elevators_info[each_lift]["lift_speed"])

                                              

        for key in floors_info:
            floor_position = floors_info[key]["graphic_position"]
            lifts_at_floor = lift_finder(floor_amount, lift_names, floor_position, elevator_speed)


            if (len(lifts_at_floor)) != 0:
                #DropOff Process
                for possible_lift in lifts_at_floor:
                    if key in elevators_info[possible_lift]["destinations"]:
                        #Elevator stopping, dropping people off and then going again
                        initial_speed = elevators_info[possible_lift]["lift_speed"]
                        elevators_info[possible_lift]["lift_speed"] = 0
                        people_drop_off(floor_amount, key, possible_lift)
                        info_present(people_amount, floor_amount, lifts_amount)
                        elevators_info[possible_lift]["lift_speed"] = initial_speed
                    full_capacity_checker(possible_lift)

                #Collection Process
                lift_options = collection_evaluator(lifts_at_floor)
                for each_lift in lift_options:
                    initial_speed = elevators_info[each_lift]["lift_speed"]
                    waiting_amount = len(floors_info[key]["people_waiting"])
                    if waiting_amount > 0:
                        #Elevator stopping, picking people up and then going again
                        elevators_info[each_lift]["lift_speed"] = 0
                        people_collection(floor_amount, key, initial_speed, each_lift)
                        info_present(people_amount, floor_amount, lifts_amount)
                        elevators_info[each_lift]["lift_speed"] = initial_speed
                    elevators_info[each_lift]["target_floor"] = new_target_assignment(lifts_amount, floor_amount,
                                                                                      each_lift, initial_speed, lift_names)
                full_capacity_checker(each_lift)



        main_window.update()
        finished_amount = int(dropped_off_count(floor_amount))






"""This function calculates whether a person wants to to go up
   or down in the building. This is calculated by working out
   if the destination floor is higher or lower than the waiting
   floor. Dependent the string content of direction_of_person
   is stored and returned at the end of the function. This
   function is ran everytime a person is created."""
def find_person_direction(waiting_floor,destination_floor):
    if destination_floor > waiting_floor:
        direction_of_person = "UP"
    elif waiting_floor > destination_floor:
        direction_of_person = "DOWN"
    return direction_of_person

"""This function allocates a person a floor. This function also
   makes sure that the destination a person is assigned is
   not equivalent to the floor they are waiting at. This function
   is ran every time a person is created."""
def floor_allocation(waiting_floor, floor_amount):
    valid_floor = None
    while valid_floor != True:
        destination = random.randint(0, (floor_amount-1))
        #Waiting Floor cant be the same as the destination
        if destination == waiting_floor:
            valid = False
        else:
            valid = True
            return destination

"""This function allocates their weight to a
   person. Firstly a list is created with all
   the possible weights. Weights closer to the
   UK average are appended more times to the list
   and weights are further away from the UK average
   are appended less. From this list an element is
   chosen at random and assigned to a person as
   their weight. This function is called everytime
   a person is created."""
def person_mass_decision():
    possible_masses = []
    for a in range(10):
        possible_masses.append(80)
    for b in range(9):
        possible_masses.append(70)
        possible_masses.append(90)
    for c in range(7):
        possible_masses.append(60)
        possible_masses.append(50)
    for d in range(5):
        possible_masses.append(40)
    for e in range(3):
        possible_masses.append(30)
        possible_masses.append(100)
        possible_masses.append(110)
    for f in range(1):
        possible_masses.append(20)
        possible_masses.append(200)
        possible_masses.append(150)
    mass_of_person = random.choice(possible_masses)
    return mass_of_person


"""This function creates all the people in the simulation.
   Each person is represented by a list containing their mass,
   destination floor, there waiting time and the direction
   they want to go in the building. The contents in the list
   are assigned by using the functions, floor_allocation,
   person_mass_decision and find_person_direction. Once this
   list is ready it is appended to the floor's people_waiting
   list they have been randomly assigned to as their waiting
   floor"""
def create_people(people_amount, floor_amount):
    for people in range(people_amount):
        #Assigns the floor the person will be waiting for
        waiting_floor = random.randint(0, (floor_amount-1))
        #Assigns the destination the person will go to
        destination_floor = floor_allocation(waiting_floor, floor_amount)
        #Assigns the person's mass
        person_mass = person_mass_decision()
        #Finds the direction the person wants to travel in
        person_direction = find_person_direction(waiting_floor, destination_floor)
        #Adds detail to array that will represent the person
        person_detail = [person_mass, destination_floor, 0, person_direction]
        #Updating Interface
        floors_info[waiting_floor]["people_waiting"].append(person_detail)
        floors_info[waiting_floor]["waiting_mass"] += person_detail[0]


"""This function enables the animation of the people that are waiting.
   The more people that are at a floor, the longer the bars are. This
   function changes the lengths of these bars when someone is picked up.
   So the function looks floors_info and looks the people_waiting. So the
   length of these bars are proportionate to the length of the people_waiting
   list for the floor. This function is ran everytime so the updated amount
   of people that are waiting can be reflected on the user interface."""
def animate_waiting_people(floor_amount):
    #Creates Bars to Represent the People Waiting
    for level in range(floor_amount):
        top_coordinate = floors_info[level]["graphic_position"]
        left_coordinate = 190 - ((len(floors_info[level]["people_waiting"]))*10)
        window_canvas.create_rectangle(left_coordinate, top_coordinate,190, (top_coordinate+15),
                                       tags="waiting_people", fill="purple")


"""This function evaluates the direction the elevator is going in.
   Depending if the speed is greater than 0 or not, will determine
   the string contents of direction_of_elevator. The string value
   of direction_of_elevator is returned at the end of the function.
   This function is called when the elevator evaluates whether to
   pick someone up or not."""
def find_elevator_direction(speed):
    if speed > 0:
        direction_of_elevator = "DOWN"
    elif speed < 0:
        direction_of_elevator = "UP"
    return direction_of_elevator


"""This function moves the necessary data to the right
   locations for the collection of a person made. Firstly
   the collection of the person is evaluated against the
   capacity of the lift. Then the direction that the person
   is compared against the direction that the elevator is going
   in. If they are the same then the collection takes place. This
   means the remaining weight on the elevator being decreased, the
   list representing the person being added to the people_there list
   for the elevator. The destination of the person is added to
   the destinations list of the elevator and then this person is
   removed from the floor. Then animate_waiting_people is called
   so the collection of this person is reflected on the UI."""
def people_collection(floor_amount, key, initial_speed, option):
    speed_change_points = [0, (floor_amount-1)]
    for person in floors_info[key]["people_waiting"]:
        #Not enough weight allowance left on the lift
        if person[0] > elevators_info[option]["remaining_weight"]:
            pass
        #There are too many people already on the lift
        if len(elevators_info[option]["people_there"]) >= 10:
            pass
        else:
            elevator_direction = find_elevator_direction(initial_speed)
            if elevator_direction == person[3] or key in speed_change_points:
                #Updating Dictionaries
                elevators_info[option]["remaining_weight"] -= person[0]
                elevators_info[option]["people_there"].append(person)
                elevators_info[option]["destinations"].append(person[1])
                floors_info[key]["people_waiting"].remove(person)
                #Updating User Interface
                window_canvas.delete("waiting_people")
                animate_waiting_people(floor_amount)
                main_window.update()


"""This function animates the amount of people that have been dropped off. The
   length of the bars is proportionate to the the length of the people_finished
   list in floors_info for the specific floor. The function extends the lengths
   of the bars when the length of the people_finished list is greater for a floor.
   This means whenever a person is dropped off this will be reflected on the UI."""
def animate_finished_people(floor_amount):
    #Creates bars for the people that have been dropped off
    for stage in range(floor_amount):
        top_coordinate = floors_info[stage]["graphic_position"]
        right_coordinate = 1110 + ((len(floors_info[stage]["people_finished"]))*10)
        window_canvas.create_rectangle(1110, top_coordinate, right_coordinate,( top_coordinate+15),
                                      tags="finished_people", fill="purple")
        


"""This function moves the necessary data to the right data
   structures for the drop-off of a person to be made. Firstly
   the person is evaluated against the current floor number to see
   if this is their destination. If so, the list that represents the
   person is appended to the people_finished list of the floor. #the
   remaining weight of the lift is incremented by the persons weight
   and the current floor number is removed from destinations. Then
   the list is removed from the people_there list in the elevator.
   Then animate_finished_people is called so the dropoff of this person
   is reflected on the UI."""    
def people_drop_off(floor_amount, key, one_lift):
    for human in elevators_info[one_lift]["people_there"]:
        if human[1] == key:
            #Updating Dictionaires
            floors_info[key]["people_finished"].append(human)
            elevators_info[one_lift]["remaining_weight"] += human[0]
            elevators_info[one_lift]["destinations"].remove(human[1])
            elevators_info[one_lift]["people_there"].remove(human)
            #Updating User Interface
            window_canvas.delete("finished_people")
            animate_finished_people(floor_amount)
            main_window.update()

