from tkinter import *
from tkinter import messagebox

                      
"""This function takes the amount of floors
   and the amount of lifts entered by the user,
   and validates this against the dictionary
   lift_amount_limits. If the user's inputs
   are consideredto create a stable model then
   the boolean content of valid_model will be
   returned as 'True'. However is the users inputs
   are considered to create an unstable model then
   the boolean content of valid_model will return as
   'False'. Also the integer value stored under
   recommended_amount will be the integer value
   stored under the 'lift_limit' key."""
def checkValidity(user_floors,user_lifts):
    valid_model = None
    lift_amount_limits = {
    1: {"floor_range":[i for i in range(1,11)], "lift_limit": 2},
    2: {"floor_range":[i for i in range(11,31)], "lift_limit": 6},
    3: {"floor_range":[i for i in range(31,51)], "lift_limit":10},
    4: {"floor_range":[i for i in range(51,71)], "lift_limit":14},
    5: {"floor_range":[i for i in range(71,90)], "lift_limit":18}
    }

    if user_floors >= 100:
        if user_lifts <= 20:
            valid_model = True
        else:
            valid_model = False
    for dict_section in range(1,6):
        if user_floors in lift_amount_limits[dict_section]["floor_range"]:
            if user_lifts <= lift_amount_limits[dict_section]["lift_limit"]:
                valid_model = True
                recommended_amount = 0
            else:
                valid_model = False
                recommended_amount = lift_amount_limits[dict_section]["lift_limit"]

    return valid_model,recommended_amount
        
    

"""This is the function that runs simulations
   of the user's configurations. Firstly the function
   catches the data the user has enetered in the
   configuration interface and converts this to
   integer data. Some of this data is put through
   checkValidity to see if the data the user has entered
   creates a stable model. If the boolean content
   returned from checkValidity is True, functions from
   personal_control_animation are executed. If the
   contents returned is False, then an error message
   is displayed which contains a new recommended
   amount of lifts for the user."""
def create_animation():
    user_lifts = int(lifts_amount.get())
    user_floors = int(floors_amount.get())
    user_people = int(people_amount.get())

    if checkValidity(user_floors, user_lifts)[0] == True:
        
        configuration_window.mainloop()

        from personal_control_animation import (create_sides,create_floors,
                                                create_people,
                                                create_multiple_elevators,
                                                animate_waiting_people,
                                                animate_finished_people)

        create_sides()
        create_floors(user_floors)
        create_people(user_people,user_floors)
        animate_waiting_people(user_floors)
        animate_finished_people(user_floors)
        create_multiple_elevators(user_people,user_floors,user_lifts)
        mainloop()

    else:
        recommended_lifts = checkValidity(user_floors, user_lifts)[1]
        messagebox.showwarning("Warning",("You have created an unstable model",
                               "Try: ",recommended_lifts," lifts instead"))
    
configuration_window = Tk()
configuration_window.title("Personal Control System Configuration")
Label(configuration_window, text="Enter the Amount of Floors: ").grid(row=0)
floors_amount = Entry(configuration_window)
floors_amount.grid(row = 0, column = 1)
Label(configuration_window, text="Enter the Amount of People: ").grid(row=1)
people_amount = Entry(configuration_window)
people_amount.grid(row = 1, column = 1)
Label(configuration_window, text="Enter the Amount of Lifts: ").grid(row=2)
lifts_amount = Entry(configuration_window)
lifts_amount.grid(row = 2, column = 1)
Button(configuration_window, 
          text='Submit', command=create_animation).grid(row=3,column=1)
                                                       







