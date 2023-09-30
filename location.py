import csv

# instantiating distance csv data as 2D array
two_dim_array = []
with open("csv/Distance.csv") as dist_file:
    for line in dist_file:
        elements = line.strip().split(',')
        two_dim_array.append(elements)

# instantiating address csv data as a list
with open("csv/Addresses.csv") as addr_file:
    address_csv = csv.reader(addr_file)
    address_csv = list(address_csv)


# using two addresses as x and y coordinates to correspond with the distance data csv
def address_distance(address_1, address_2):
    distance = two_dim_array[address_1][address_2]
    if distance == '':
        distance = two_dim_array[address_2][address_1]

    return float(distance)


# function for retrieving package addresses from address csv
def get_address(address):
    for row in address_csv:
        if address in row[2]:
            return int(row[0])
