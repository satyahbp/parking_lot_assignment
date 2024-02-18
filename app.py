from dotenv import load_dotenv
load_dotenv()

from scripts.core.handlers.parking_handler import ParkingClass
from scripts.constants.app_constants import improper_command_message

parking_obj = ParkingClass()


if __name__ == "__main__":
    print("Welcome to Satya's Parking Lot! ")
    print("Enter Your Command (Type 'help' to get all the commands).")
    while(True):
        command = input("Enter Command> ")
        command = command.split()
        if not command:
            continue

        # for help
        if command[0].lower() == "help":
            if len(command) != 1:
                print(improper_command_message)
                continue
            parking_obj.print_command_list()

        # for creating a parking lot
        elif command[0].lower() == "create_parking_lot":
            if len(command) != 2:
                print(improper_command_message)
                continue
            parking_obj.start(command[1])

        # for parking
        elif command[0].lower() == "park":
            if len(command) != 3:
                print(improper_command_message)
                continue
            parking_obj.add_car(command[1], command[2])
        
        # for leaving parking
        elif command[0].lower() == "leave":
            if len(command) != 2:
                print(improper_command_message)
                continue
            parking_obj.remove_car(command[1])
        
        # for status
        elif command[0].lower() == "status":
            if len(command) != 1:
                print(improper_command_message)
                continue
            parking_obj.check_status()

        # registration numbers of all cars of a particular color
        elif command[0].lower() == "registration_numbers_for_cars_with_colour":
            if len(command) != 2:
                print(improper_command_message)
                continue
            parking_obj.car_number_from_color(command[1])
        
        # slot number in which a car with a given registration number is parked.
        elif command[0].lower() == "car_slot":
            if len(command) != 2:
                print(improper_command_message)
                continue
            parking_obj.find_slot_from_car_number(command[1])
        
        # slot numbers in which cars of a particular color are parked
        elif command[0].lower() == "color_slot":
            if len(command) != 2:
                print(improper_command_message)
                continue
            parking_obj.find_car_slots_from_color(command[1])
        
        # to exit the program
        elif command[0].lower() == "exit":
            if len(command) != 1:
                print(improper_command_message)
                continue
            parking_obj.exit_parking()
            break
        
        # in case of wrong commands
        else:
            print(improper_command_message)
            
            

            