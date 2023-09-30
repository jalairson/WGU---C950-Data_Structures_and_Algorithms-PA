import csv


class Package(object):

    # package constructor
    def __init__(self, id, address, city, state, zip, deadline, weight, instructions, status, departure, arrival):
        self.id = id  # package ID (index 0 in csv)
        self.address = address  # package delivery address (index 1 in csv)
        self.city = city  # package address city (index 2 in csv)
        self.state = state  # package address state (index 3 in csv)
        self.zip = zip  # package address zipcode (index 4 in csv)
        self.deadline = deadline  # package delivery deadline (index 5 in csv)
        self.weight = weight  # package weight (index 6 in csv)
        self.instructions = instructions  # special instructions (index 7 in csv)
        self.status = status  # package transit status
        self.departure = departure  # package departure time
        self.arrival = arrival  # package arrival time

    # package string formatting
    def __str__(self):
        return '(1) %s | (2) %s | (3) %s, %s | (4) %s | (5) %s | (6) %s | (7) %s | (8) %s | (9) %s | (10) %s' % (
            self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.instructions,
            self.status, self.departure, self.arrival
        )

    # branching statement for easy status updates
    def set_status(self, del_status):
        if del_status == 1:
            self.status = 'DELIVERED'
        elif del_status == 0:
            self.status = 'OUT FOR DELIVERY'
        else:
            self.status = 'AT HUB'


# package csv loading to insert package data into hash table (req. A)
def load_package_data(package_file, hash_table):
    with open(package_file) as PackageCSV:
        package_data = csv.reader(PackageCSV, delimiter=',')
        for packageLn in package_data:
            p_id = int(packageLn[0])
            p_address = packageLn[1]
            p_city = packageLn[2]
            p_state = packageLn[3]
            p_zip = packageLn[4]
            p_deadline = packageLn[5]
            p_weight = packageLn[6]
            p_instructions = packageLn[7]
            p_status = "AT HUB"
            p_departure = None
            p_arrival = None

            # package object
            package = Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_weight, p_instructions, p_status,
                              p_departure, p_arrival)
            # inserts package information into chaining hash table
            hash_table.insert(p_id, package)
