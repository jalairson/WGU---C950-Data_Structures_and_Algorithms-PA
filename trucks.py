# initializing constructor for truck objects
class Truck(object):
    def __init__(self, deliveries, curr_address, curr_time, depart_time, miles_traveled):
        self.deliveries = deliveries
        self.curr_time = curr_time
        self.depart_time = depart_time
        self.curr_address = curr_address
        self.miles_traveled = miles_traveled
        return

    # string constructor for printing truck information
    def __str__(self):
        return '%s, %s, %s, %s, %s' % (
            self.deliveries, self.curr_time, self.depart_time,
            self.curr_address, self.miles_traveled
        )


# a fetching function to retrieve truck package lists in main
def get_truck_list(truck_id):
    # manual loading package index lists for all three trucks
    truck_one_list = [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40]
    truck_two_list = [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39]
    truck_three_list = [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33]
    # passing an integer as truck ID
    if truck_id == 1:
        return truck_one_list
    if truck_id == 2:
        return truck_two_list
    if truck_id == 3:
        return truck_three_list
    else:
        return "There is no such truck in service"


def check_truck_list(package_id):
    if package_id in get_truck_list(1):
        return 'truck one'
    elif package_id in get_truck_list(2):
        return 'truck two'
    elif package_id in get_truck_list(3):
        return 'truck three'
    else:
        return 'UNKNOWN'
