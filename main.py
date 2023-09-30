# Jeremiah Lairson
# student ID: 009965674

import datetime
# I blocked out this import because pyfiglet is not a native library,
# but you can see the effect in the UI screenshot
# import pyfiglet

from hashTable import ChainingHashTable
from location import address_distance, get_address
from package import load_package_data
from trucks import Truck, get_truck_list, check_truck_list

# storing current date for user
current_datetime = datetime.datetime.now()
current_date = current_datetime.date()
formatted_date = current_datetime.strftime("%B %d, %Y")

# instantiating package hash table
package_hash_table = ChainingHashTable()

# send package data to package hash table
load_package_data("csv/Packages.csv", package_hash_table)

# instantiating truck objects with truck package lists
truck1 = Truck(get_truck_list(1), "4001 South 700 East", datetime.timedelta(hours=8, minutes=0), datetime.timedelta(hours=8, minutes=0), 0.0)
truck2 = Truck(get_truck_list(2), "4001 South 700 East", datetime.timedelta(hours=10, minutes=20), datetime.timedelta(hours=10, minutes=20), 0.0)
truck3 = Truck(get_truck_list(3), "4001 South 700 East", datetime.timedelta(hours=9, minutes=5), datetime.timedelta(hours=9, minutes=5), 0.0)


# ---hash table test---
# print(package_hash_table.lookup(26))
# print(package_hash_table.lookup(41))

# ---2D array parsing test---
# print(two_dim_array[26][0])

# package distribution algorithm definition with argument of truck ID
def delivery_engine(t_id):
    to_deliver = []
    t_id.curr_time = t_id.depart_time
    # parse packages on each truck by package ID
    for p_id in t_id.deliveries:
        # extract package information by package ID
        package = package_hash_table.lookup(p_id)
        # setting the package status for all packages as "out for delivery"
        # updating the time of departure for packages to match the time for the truck
        package.set_status(0)
        package.departure = t_id.depart_time
        # using a list of packages to yet to be delivered on the truck
        to_deliver.append(package)
    t_id.deliveries.clear()
    # clear loaded packages list to transfer packages from one list to the next as they are delivered

    # running a loop while any packages are still on the truck and the distance is less within 20 miles
    while len(to_deliver) > 0:
        next_addr = 20
        next_pkg = None
        # using address_distance function to obtain the corresponding distance
        # using two addresses from the address table
        for package in to_deliver:
            if address_distance(get_address(t_id.curr_address), get_address(package.address)) <= next_addr:
                # defining address and package logistical positions
                next_addr = address_distance(get_address(t_id.curr_address), get_address(package.address))
                next_pkg = package
                # removing package from awaiting list and adding it to completed list
        t_id.deliveries.append(next_pkg.id)
        to_deliver.remove(next_pkg)
        # adding the distance to each stop to the total miles traveled counter for the truck object
        t_id.miles_traveled += next_addr
        # iterating stops
        t_id.curr_address = next_pkg.address
        # assigning the time of each delivery using the truck departure time, travel speed, and travel distance
        t_id.curr_time += datetime.timedelta(hours=next_addr / 18.0)
        # updating status, truck departure time, and package arrival time for each package
        next_pkg.arrival = t_id.curr_time
        next_pkg.depart_time = t_id.depart_time
        next_pkg.set_status(1)


def package_time_status(user_time, pack_id):
    user_package = package_hash_table.lookup(pack_id)
    if user_time < user_package.departure:
        return 'AT HUB'
    elif user_package.departure <= user_time < user_package.arrival:
        return 'OUT FOR DELIVERY'
    elif user_time >= user_package.arrival:
        return 'DELIVERED'


# UI section of the application (req. D)
# Begins prompting
# font = pyfiglet.Figlet(font='standard')
# print(font.renderText('-- WGUPS --'))
print()
print("--Welcome to the WGUPS delivery tracking system!--")
print()

# running the delivery algorithm for each truck object
delivery_engine(truck1)
delivery_engine(truck2)
# staggering truck departure times
truck3.depart_time = min(truck1.curr_time, truck2.curr_time)
delivery_engine(truck3)

print("##################################################################")
# simple terminal navigation menu using branching
print("please enter a numeric value to navigate:")
print("1) Package tracking by package ID#; tracking by time of day")
print("2) Package list by truck ID#")
print("3) Display all scheduled package deliveries")
print("4) Display distance for each/all trucks")
print("##################################################################")
# removed option 4 while option 1 now accounts for time input
# print("4) Display all packages within a specific time interval")

user_nav = int(input())

if user_nav == 1:
    # option 1 prints from the package hash table using a package ID number
    print("* To locate a package by the associated ID number, please enter the associated ID number now.")
    print("#############################################################################################")
    user_pkg_id = int(input())
    # validate package ID
    if 0 < user_pkg_id <= 40:
        print("(1) ID | (2) ADDRESS | (3) CITY, STATE, ZIP | (5) DUE_BY | (6) PARCEL_WEIGHT_KG")
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
        usr_pkg = package_hash_table.lookup(user_pkg_id)
        print("ID: " + str(usr_pkg.id) + "; " + usr_pkg.address + " " + usr_pkg.city + ", " + usr_pkg.state + " "
              + usr_pkg.zip + "; due by " + usr_pkg.deadline + "; weight: " + usr_pkg.weight + "kg")
        print("Carried on " + check_truck_list(usr_pkg.id))
        print("Special instructions for handling: " + usr_pkg.instructions)
        print("To check the status of the package at a specified time:")
        print("Please provide time: HOURS")
        user_hour = int(input())
        print("Please provide time: MINUTES")
        user_minutes = int(input())
        user_check_time = datetime.timedelta(hours=user_hour, minutes=user_minutes)
        user_status = package_time_status(user_check_time, usr_pkg.id)
        print("Status for package " + str(usr_pkg.id) + " at " + str(user_check_time))
        print("Package #" + str(usr_pkg.id) + ", " + user_status, end=' ')
        if user_status == 'DELIVERED':
            print("at " + str(usr_pkg.arrival) + " to " + usr_pkg.address)
            print()
        elif user_status == 'OUT FOR DELIVERY':
            print("as of " + str(usr_pkg.departure))
            print()
        elif user_status == 'AT HUB':
            print("; Departing at " + str(usr_pkg.departure))
            print()
    # contingency print statement on validation
    else:
        print("There is no tracked package with the associated ID number.")

elif user_nav == 2:
    # option 2 prints all information for every package on a particular truck, selecting by truck number
    print("* to list package IDs on truck by truck ID number, please enter the associated truck ID now.")
    print("############################################################################################")
    user_truck_id = int(input())
    print("Please provide time: HOURS")
    usr_hrs = int(input())
    print("Please provide time: MINUTES")
    usr_mins = int(input())
    usr_tm_chk = datetime.timedelta(hours=usr_hrs, minutes=usr_mins)
    # validate truck number
    if 0 < user_truck_id <= 3:
        print("packages on truck " + str(user_truck_id) + ":")
        print("####################################################################")
        for element in get_truck_list(user_truck_id):
            base_pkg = package_hash_table.lookup(element)
            stats = package_time_status(usr_tm_chk, base_pkg.id)
            print("ID: " + str(base_pkg.id) + "; " + base_pkg.address + " " + base_pkg.city + ", " + base_pkg.state
                  + " " + base_pkg.zip + "; due by " + base_pkg.deadline + "; weight: " + base_pkg.weight + "kg")
            print("Carried on " + check_truck_list(base_pkg.id))
            print("Special instructions for handling: " + base_pkg.instructions)
            print(stats, end=' ')
            if stats == 'DELIVERED':
                print("at " + str(base_pkg.arrival) + " to " + base_pkg.address)
                print()
            elif stats == 'OUT FOR DELIVERY':
                print("as of " + str(base_pkg.departure))
                print()
            elif stats == 'AT HUB':
                print("; Departing at " + str(base_pkg.departure))
                print()
    # contingency print statement on validation
    else:
        print("Invalid truck ID")

elif user_nav == 3:
    # option 3 prints all packages scheduled for delivery across all trucks
    print("Enter time specification")
    print("Enter time HOURS:")
    time_pt_hr = int(input())
    print("Enter time MINUTES:")
    time_pt_min = int(input())
    time_pt = datetime.timedelta(hours=time_pt_hr, minutes=time_pt_min)
    print("All packages scheduled for delivery by EOD on " + str(formatted_date) + ":")
    print(
        "-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for package_id in range(1, 41):
        package_info = package_hash_table.lookup(package_id)
        print("ID: " + str(package_info.id) + "; " + package_info.address + " " + package_info.city + ", " + package_info.state + " "
              + package_info.zip + "; due by " + package_info.deadline + "; weight: " + package_info.weight + "kg")
        print("Carried on " + check_truck_list(package_info.id))
        print("Special instructions for handling: " + package_info.instructions)
        third_stats = package_time_status(time_pt, package_info.id)
        print(third_stats, end=' ')
        if third_stats == 'DELIVERED':
            print("at " + str(package_info.arrival) + " to " + package_info.address)
            print()
        elif third_stats == 'OUT FOR DELIVERY':
            print("as of " + str(package_info.departure))
            print()
        elif third_stats == 'AT HUB':
            print("; Departing at " + str(package_info.departure))
            print()
# Changed branch 4 to list mileage/distance info for trucks instead of displaying it in the main menu
elif user_nav == 4:
    print("1) Display mileage for truck 1")
    print("2) Display mileage for truck 2")
    print("3) Display mileage for truck 3")
    print("4) Display mileage for all trucks")

    truck_nav = int(input())

    if truck_nav == 1:
        print(f"Truck 1: {truck1.miles_traveled:.1f}")

    if truck_nav == 1:
        print(f"Truck 2: {truck2.miles_traveled:.1f}")

    if truck_nav == 3:
        print(f"Truck 3: {truck3.miles_traveled:.1f}")

    if truck_nav == 4:
        print("Today's total distance (miles) for all current delivery routes: " + str(
            truck1.miles_traveled + truck2.miles_traveled + truck3.miles_traveled))
