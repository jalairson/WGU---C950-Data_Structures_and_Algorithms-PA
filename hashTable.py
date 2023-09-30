# assignment prompt: section A hash table data structure + section B lookup function

'''
A.  Develop a hash table, without using any additional libraries or classes, that has an insertion function that takes the package ID as input and inserts each of the following data components into the hash table:
•   delivery address
•   delivery deadline
•   delivery city
•   delivery zip code
•   package weight
•   delivery status (i.e., at the hub, en route, or delivered), including the delivery time
'''


# Hash table using chaining as shown in Cemal Tepe's hash tables webinar
class ChainingHashTable():
    # constructor with optional initial capacity parameter
    # assigns all buckets with an empty list
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries
        self.initial_capacity = initial_capacity
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # to insert new item into hash table
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if already in bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert item to end of bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # (req. B) lookup method for k,v pair (used to return package info by package ID)
    def lookup(self, key):
        # get the bucket list where this key would be
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key > len(self.table):
            return "--package information could not be found--"

        # search for key in bucket list
        for key_value in bucket_list:
            # print (key_value
            if key_value[0] == key:
                return key_value[1]  # value
            return None

    # edited remove method for k, v pair
    def remove(self, key):
        # get bucket list where item will be removed
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove item from the list if present
        for kv in bucket_list:
            # print(key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
