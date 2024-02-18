from prettytable import PrettyTable

from scripts.logging.log_module import logger as log
from scripts.utils.mongo_utility import MongoUtility
from scripts.constants.app_configuration import MONGO_HOST, MONGO_PORT, PARKING_DB, PARKING_COLLECTION

class ParkingClass():

    def __init__(self) -> None:
        self.mongo_obj = MongoUtility(MONGO_HOST, MONGO_PORT)

    
    @staticmethod
    def print_command_list():
        # message
        print("\nWhile entering a command, leave 1 blank space before each input/argument for the command.\n")

        # create_parking_lot command
        print("\u2022 create_parking_lot <input_1 - number of slots>")
        print("Creates the parking lot with specified number of slots.\n")

        # park
        print("\u2022 park <input_1 - car_number> <input_2 - car color>")
        print("Adds car to the nearest available slot\n")

        # leave
        print("\u2022 leave <input_1 - slot to vacate>")
        print("Vacates the specified slot.\n")

        # status
        print("\u2022 status")
        print("Prints the status of the cars. Does not require any input/argument.\n")

        # registration_numbers_for_cars_with_colour
        print("\u2022 registration_numbers_for_cars_with_colour <input_1 - color of car>")
        print("Prints the car numbers present in the parking lot for the specified color.\n")

        # car_slot
        print("\u2022 car_slot <input_1 - car number>")
        print("Prints the slot in which the car of the specified number is parked.\n")

        # color_slot
        print("\u2022 color_slot <input_1 - color>")
        print("Prints the slots in which cars of specified color are parked.\n")

        # help
        print("\u2022 help")
        print("Prints the list of commands and their inputs/arguments required for the program. Does not require any input/argument.\n")

        # exit
        print("\u2022 exit")
        print("Exits the program, deletes the parking lot. Does not require any input/argument.\n")


    def start(self, number_of_slots: int) -> None:
        # to create empty slots
        try:
            try:
                number_of_slots = int(number_of_slots)                
            except:
                print("Please enter valid number of slots.")
                return
            
            if number_of_slots < 1:
                print("Please enter valid number of slots.")
                return
            
            # checking whether table exists:
            table_status = self.mongo_obj.check_table_existence(PARKING_DB, PARKING_COLLECTION)
            if table_status:
                print("Parking lot already exists!")
                return
            
            # creating empty slots
            print(f"Creating slots: {number_of_slots}")
            slot_list = list()
            for i in range(1, number_of_slots + 1):
                slot_list.append({
                    "slot_no": i,
                    "car_no": "",
                    "car_color": ""
                })
            
            # inserting empty slots into mongodb
            status = self.mongo_obj.bulk_insert(
                db_name=PARKING_DB,
                collection_name=PARKING_COLLECTION,
                dict_list=slot_list
            )

            if status:
                print(f"Created a parking lot with {number_of_slots} slots")
            else:
                print("Could not create a parking lot, please try again!")
        except Exception as e:
            log.error(str(e))


    def add_car(self, car_no: str, car_color: str) -> None:
        # This function will add the car wherever it will find the 
        # slot empty nearest to the entry point.
        # If no slot is availble, it will not allot any slot.
        try:
            if not isinstance(car_no, str):
                print("Please insert proper car number.")
                return
            if not isinstance(car_color, str):
                print("Please insert proper car color.")
                return
            
            # checking whether table exists:
            table_status = self.mongo_obj.check_table_existence(PARKING_DB, PARKING_COLLECTION)
            if not table_status:
                print("No Parking Lot found. Please create one. Type 'help' to get the commands and their inputs.")
                return
            
            # fetching empty slot
            empty_slot_query = {"car_no": ""}
            empty_slot = self.mongo_obj.fetch_using_query(
                db_name=PARKING_DB,
                collection_name=PARKING_COLLECTION,
                query=empty_slot_query,
                limit=1,
                sort="slot_no",
                sort_order=1
            )

            # if no slot is found
            if not empty_slot:
                print("Sorry, parking lot is full.")
                return
            
            empty_slot = empty_slot[0]
            update_dict={
                "car_no": car_no,
                "car_color": car_color
            }
            update_query = {"slot_no": empty_slot["slot_no"]}
            update_status = self.mongo_obj.update_one(
                db_name=PARKING_DB,
                collection_name=PARKING_COLLECTION,
                update_query=update_query,
                update_dict=update_dict
            )

            if update_status:
                print(f'Alloted slot number: {empty_slot["slot_no"]}')
            else:
                print("Unable to allot slot. Please try again.")
            
        except Exception as e:
            log.error(str(e))

    
    def remove_car(self, slot_no: int) -> None:
        # This function removes the car from the slot number 
        # given in the input.
        try:

            # if invalid slot number is entered
            try:
                slot_no = int(slot_no)
            except:
                print("Please enter a valid slot number.")
                return
            
            if slot_no < 1:
                print("Please enter a valid slot number.")
                return
            
            # checking whether table exists:
            table_status = self.mongo_obj.check_table_existence(PARKING_DB, PARKING_COLLECTION)
            if not table_status:
                print("No Parking Lot found. Please create one. Type 'help' to get the commands and their inputs.")
                return

            # checking existence of slot
            count_query = {"slot_no": slot_no}
            count = self.mongo_obj.count(
                db_name=PARKING_DB,
                collection_name=PARKING_COLLECTION,
                count_query=count_query
            )
            # if slot doesn't exist
            if count == 0:
                print(f"Slot No. {slot_no} does not exist.")
                return
            
            # vacating the slot
            update_dict = {
                "car_no": "",
                "car_color": ""
            }
            update_status = self.mongo_obj.update_one(
                db_name=PARKING_DB,
                collection_name=PARKING_COLLECTION,
                update_query=count_query,
                update_dict=update_dict
            )

            if update_status:
                print(f"Slot number {slot_no} is free.")
            else:
                print(f"Could not free slot no {slot_no}. Please try again.")

        except Exception as e:
            log.error(str(e))


    def check_status(self) -> None:
        # prints a table showing status of the cars
        try:
            # checking whether table exists:
            table_status = self.mongo_obj.check_table_existence(PARKING_DB, PARKING_COLLECTION)
            if not table_status:
                print("No Parking Lot found. Please create one. Type 'help' to get the commands and their inputs.")
                return
            
            fetch_query = {"car_no": {"$ne": ""}}
            full_slots = self.mongo_obj.fetch_using_query(
                db_name=PARKING_DB,
                collection_name=PARKING_COLLECTION,
                query=fetch_query,
                sort="slot_no",
                sort_order=1
            )

            table_to_print = PrettyTable(["Slot No.", "Registration No.", "Color"])
            for each_slot in full_slots:
                table_to_print.add_row([each_slot["slot_no"], each_slot["car_no"], each_slot["car_color"]])

            print(table_to_print)
            
        except Exception as e:
            log.error(str(e))

    
    def car_number_from_color(self, color: str) -> None:
        # prints the list of car numbers that are there in parking lot for each color
        try:
            # checking whether table exists:
            table_status = self.mongo_obj.check_table_existence(PARKING_DB, PARKING_COLLECTION)
            if not table_status:
                print("No Parking Lot found. Please create one. Type 'help' to get the commands and their inputs.")
                return
            
            # querying cars based on color (case insensitive regex query)
            color_query = {"car_color": {"$regex": f"^{color}$", "$options": "i"}}
            cars_with_color = self.mongo_obj.fetch_using_query(
                PARKING_DB,
                PARKING_COLLECTION,
                query=color_query,
                sort="slot_no",
                sort_order=1
            )

            # if no car of such color exist
            if not cars_with_color:
                print(f"No car with of {color} color exists in the parking lot.")
                return
            
            # listing down the car numbers
            cars_list = list()
            for each_car in cars_with_color:
                cars_list.append(each_car["car_no"])

            print(f"List of {color} cars in the parking lot:", ", ".join(cars_list))
        except Exception as e:
            log.error(str(e)) 


    def find_slot_from_car_number(self, car_no: str) -> None:
        # prints the slot of car of a particular number parked in the parking lot
        try:
            # checking whether table exists:
            table_status = self.mongo_obj.check_table_existence(PARKING_DB, PARKING_COLLECTION)
            if not table_status:
                print("No Parking Lot found. Please create one. Type 'help' to get the commands and their inputs.")
                return

            # querying about the car based on car no:
            car_no_query = {"car_no": car_no}
            cars_with_no = self.mongo_obj.fetch_using_query(
                PARKING_DB,
                PARKING_COLLECTION,
                query=car_no_query,
                limit=1,
                sort="slot_no",
                sort_order=1
            )

            # if no car with the number is found
            if not cars_with_no:
                print(f"No car of number {car_no} exists in the parking lot.")
                return

            print(f"The car with number {car_no} is parked in Slot {cars_with_no[0]['slot_no']}")

        except Exception as e:
            log.error(str(e))


    def find_car_slots_from_color(self, color: str) -> None:
        # prints the list of car slots that are there in parking lot for each color
        try:
            # checking whether table exists:
            table_status = self.mongo_obj.check_table_existence(PARKING_DB, PARKING_COLLECTION)
            if not table_status:
                print("No Parking Lot found. Please create one. Type 'help' to get the commands and their inputs.")
                return
            
            # querying cars based on color (case insensitive regex query)
            color_query = {"car_color": {"$regex": f"^{color}$", "$options": "i"}}
            cars_with_color = self.mongo_obj.fetch_using_query(
                PARKING_DB,
                PARKING_COLLECTION,
                query=color_query,
                sort="slot_no",
                sort_order=1
            )

            # if no car of such color exist
            if not cars_with_color:
                print(f"No car with of {color} color exists in the parking lot.")
                return
            
            # listing down the car numbers
            cars_list = list()
            for each_car in cars_with_color:
                cars_list.append(str(each_car["slot_no"]))

            print(f"Slots of {color} cars in the parking lot:", ", ".join(cars_list))
        except Exception as e:
            log.error(str(e)) 

    
    def exit_parking(self) -> None:
        try:
            self.mongo_obj.delete_collection(PARKING_DB, PARKING_COLLECTION)
            print("Closing parking lot.")
        except Exception as e:
            log.error(str(e))