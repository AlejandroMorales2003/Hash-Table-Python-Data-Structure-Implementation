# Name: Alejandro Morales
# OSU Email: moralea3@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignments 6
# Due Date: 9 Aug 2022
# Description: Creates the hash map data strucutr using open adressing
from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)
class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._hash_function = function
        self._size = 0
    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out
    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1
        while not self._is_prime(capacity):
            capacity += 2
        return capacity
    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True
        if capacity == 1 or capacity % 2 == 0:
            return False
        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2
        return True
    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size
    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity
    # ------------------------------------------------------------------ #
    def put(self, key: str, value: object) -> None:
        '''
        puts an element into the hash table based on the hash function

        :param value: a string and an object

        :return: nothing

        '''	

        #gets the table load
        load = self.table_load()
        
        #checks the conditions of the table load
        if(load >= 0.5):
            #resizes the table
            self.resize_table(self._capacity)

        #gets the hashvalue index
        hashvalue = self._hash_function(key) % self.get_capacity()

        #creates a hash entry for the new value
        newValue = HashEntry(key,value)

        #sets up quad probing
        j = 1

        #stores the original hash value
        ogHash = hashvalue

        #finds a place to put the value that is empty
        while self._buckets[hashvalue] is not None and self._buckets[hashvalue].is_tombstone == False:
            #checks if the key already exists
            if(self._buckets[hashvalue].key == newValue.key):
                #updats the value
                self._buckets[hashvalue] = newValue
                return
            
            #if a value is already there, use quad probing
            hashvalue = ogHash + pow(j,2)

            #increaments the probing value
            j+=1

            #if it's out of bounds, adjust based on the capcity
            if(hashvalue >= self._capacity):
                hashvalue = hashvalue % self._capacity

        #puts the value into place
        self._buckets[hashvalue] = newValue

        #incrment the size
        self._size+=1

    def table_load(self) -> float:
        '''
        gets the load factor for the hash table

        :param value: none

        :return: a float

        '''	
        #calculates the loadfactor
        loadfactor = float(self.get_size()/self.get_capacity())

        return loadfactor
    
    def empty_buckets(self) -> int:
        '''
        checks for the number of empty buckets in the hash table

        :param value: none

        :return: an integer

        '''	
        #sets the count for the number of empty buckets
        count = 0 

        #iterates through the hash table to check if they're empty
        for x in range(self.get_capacity()):
            #checks if they're empty
            if(self._buckets[x] is None):
                #increments the count
                count+=1

        return count

    def resize_table(self, new_capacity: int) -> None:
        '''
        resizes the hash table

        :param value: an integer

        :return: nothing

        '''	

        #gets the table load
        load = self.table_load()
        
        #if the new capcity is less than the size, it does nothing
        if(new_capacity < self._size):
            return
        
        #variable for the new_capicty
        new = new_capacity
        
        #gets another load for the special case
        sepLoad = float(self.get_size()/new_capacity)

        #if the capacities are the same, double the capacity
        if(new_capacity == self._capacity):
            new = new_capacity * 2

        #if it's the special case, double capicty of the new capcacity
        elif(new_capacity < self._capacity and new_capacity > self._size and sepLoad >= 0.5):

            new = self._next_prime(new_capacity * 2)
        
        #storage array
        store = DynamicArray()

        #iterates through the hash table
        for x in range(self._capacity):
            #if the buckets are not empty
            if self._buckets[x] is not None:
                #appends to the storage
                store.append(self._buckets[x])

        #reintializes the function with the new capacity
        self.__init__(new,self._hash_function)

        #puts the values back into the hash table from the storage array
        for x in range(store.length()):
            self.put(store[x].key,store[x].value)

    def get(self, key: str) -> object:
        '''
        gets the value from a key

        :param value: a string

        :return: an object

        '''	

        #defaults the value to none in case of no element being found
        value = None

        #iterates through the array
        for x in range(self._capacity):
            #finds the value
            if(self._buckets[x] is not None and self._buckets[x].key == key and self._buckets[x].is_tombstone == False):
                return self._buckets[x].value
    
    def contains_key(self, key: str) -> bool:
        '''
        determines if there is a key

        :param value: a string

        :return: a boolean

        '''	
        #intializes it to false in case the value is not found
        value = False
        #iterates through the array
        for x in range(self._capacity):
            #finds the key
            if(self._buckets[x] is not None and self._buckets[x].key == key):
                return True
        return value
        
    def remove(self, key: str) -> None:

        #iterates through the array
        for x in range(self._capacity):
            #finds the key
            if(self._buckets[x] is not None and self._buckets[x].key == key  and self._buckets[x].is_tombstone == False):
                #sets the tombstone
                self._buckets[x].is_tombstone = True
                #decrements the size
                self._size-=1
                return

    def clear(self) -> None:
        '''
        clears the hash table

        :param value: none

        :return: nothing

        '''	

        #clears the table
        self.__init__(self.get_capacity(),self._hash_function)

    def get_keys_and_values(self) -> DynamicArray:
        '''
        gets every key and value pair from the hash table

        :param value: nothing

        :return: a filled dynamic array

        '''	
        
        #storeage array
        store = DynamicArray()

        #iterates through the hash table
        for x in range(self._capacity):
            #finds the pairs that are not empty
            if self._buckets[x] is not None and self._buckets[x].is_tombstone == False:
                #creates the tuple
                element = (self._buckets[x].key,self._buckets[x].value)
                #appends the element to the storage array
                store.append(element)

        return store

# ------------------- BASIC TESTING ---------------------------------------- #
if __name__ == "__main__":
    '''
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), 
m.get_capacity())
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), 
m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))
    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    '''

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    for capacity in range(111, 1000, 117):
        print("woah")
        m.resize_table(capacity)
        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n" f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')
        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), 
round(m.table_load(), 2))
    '''
    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))
    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))
    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')
    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())
    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())
    m.resize_table(2)
    print(m.get_keys_and_values())
    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
    '''