# Name: Alejandro Morales
# OSU Email: moralea3@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignments 6
# Due Date: 9 Aug 2022
# Description: Creates the hash map data strucutr using linked lists
from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)
class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
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
        Increment from given number and the find the closest prime number
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

        #gets the hash value index
        hashvalue = self._hash_function(key) % self.get_capacity()

        #if the key aleady exits, it updates the value
        if(self._buckets[hashvalue].length() >= 1) and self._buckets[hashvalue].contains(key) is not None:
            #gets the specific key that is a duplicate
            node = self._buckets[hashvalue].contains(key)
            #updates the value
            node.value = value
            return
        
        #when it's a new key, it adds a new element into the hash table
        else:
            self._buckets[hashvalue].insert(key,value)
            #increments the size
            self._size+=1    

    def put2(self, key: str, value: object) -> None:
        '''
        puts an element into the hash table based on the hash function for the mode function
        for for frequency

        :param value: a string and an object

        :return: nothing

        '''	
        #gets the hash value index
        hashvalue = self._hash_function(key) % self.get_capacity()
        
        #if the key aleady exits, it updates the value
        if(self._buckets[hashvalue].length() >= 1) and self._buckets[hashvalue].contains(key) is not None:

            #gets the specific key that is a duplicate
            node = self._buckets[hashvalue].contains(key)

            #increments the frequency of the key
            node.value+=1
            return
        
        #when it's a new key, it adds a new element into the hash table
        else:
            self._buckets[hashvalue].insert(key,value)
            #increments the size
            self._size+=1   

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
            if(self._buckets[x].length() == 0):
                #increments the count
                count+=1

        return count

    def table_load(self) -> float:
        '''
        gets the load factor for the hash table

        :param value: none

        :return: a float

        '''	
        #calculates the loadfactor
        loadfactor = float(self.get_size()/self.get_capacity())

        return loadfactor

    def clear(self) -> None:
        '''
        clears the hash table

        :param value: none

        :return: nothing

        '''	

        #clears the table
        self.__init__(self.get_capacity(),self._hash_function)

        return None

    def resize_table(self, new_capacity: int) -> None:
        '''
        resizes the hash table

        :param value: an integer

        :return: nothing

        '''	

        #error checks for a correct capcity
        if(new_capacity < 1):
            return

        #keeps the old capacity
        oldCap = self._capacity

        #variable for the new capacity
        new = new_capacity

        #array that stores the data from the old hash table
        store = DynamicArray()

        #iterates through the old has table
        for x in range(oldCap):
            #checks if the bucket is empty
            if(self._buckets[x].length() != 0):
                node = self._buckets[x]
                #appends the list to the store array
                store.append(node)
                #self._buckets[x] = LinkedList()

        #special case where the prime is 2
        if(new_capacity == 2):
            #clears the array
            self._buckets = DynamicArray()
            #sets the capacity
            self._capacity = 2
            #appends a list to the hash table
            for _ in range(self._capacity):
                self._buckets.append(LinkedList())
            #sets the size
            self._size = 0

        #reinitilizae, with the new capacity and hash function
        else:
            self.__init__(new,self._hash_function)

        #iterates through the storage array
        for x in range(store.length()):
            #iterates thorugh the linked lists
            for y in store[x]:
                #puts the items in the new hash table
                self.put(y.key, y.value)

    def get(self, key: str) -> object:
        '''
        gets the value from a key

        :param value: a string

        :return: an object

        '''	
        #gets the hash value index
        hashvalue = self._hash_function(key) % self.get_capacity()

        #defaults the value to none in case of no element being found
        value = None

        #finds the value
        if(self._buckets[hashvalue] is not None and self._buckets[hashvalue].contains(key) != None):
            #gets the node from the linked list
            node = self._buckets[hashvalue].contains(key)
            #gets the value from the node
            value = node.value
            return value   
        return value

    
    def contains_key(self, key: str) -> bool:
        '''
        determines if there is a key

        :param value: a string

        :return: a boolean

        '''	
        #gets the hash value index
        hashvalue = self._hash_function(key) % self.get_capacity()

        #intializes it to false in case the value is not found
        value = False

        #finds the value
        if(self._buckets[hashvalue] is not None and self._buckets[hashvalue].contains(key) != None):
            return True
        return value

        
    def remove(self, key: str) -> None:
        '''
        removes a key from the hash table

        :param value: a string

        :return: nothing

        '''	
        #gets the hash value index
        hashvalue = self._hash_function(key) % self.get_capacity()   

        #finds the index to remove 
        if(self._buckets[hashvalue] is not None and self._buckets[hashvalue].contains(key) != None):
            #removes the element
            self._buckets[hashvalue].remove(key)
            #decrements the size
            self._size-=1  

        return  

    def get_keys_and_values(self) -> DynamicArray:
        '''
        gets every key and value pair from the hash table

        :param value: nothing

        :return: a filled dynamic array

        '''	

        #storage array
        store = DynamicArray()

        #iterates through the hash table
        for x in range(self._capacity):
            #checks if it's empty
            if self._buckets[x].length() != 0:
                #iterates through the linked list
                for y in self._buckets[x]:
                    #creates a tuple
                    element = (y.key,y.value)
                    #appends the elements to the array
                    store.append(element)
    
        return store
def find_mode(da: DynamicArray) -> (DynamicArray, int):
    '''
    finds the mode of a given dynamic array

    :param value: a filled dynamic array

    :return: a filled dynamic array, and integer

    '''	

    #creates a hash table
    map = HashMap(da.length(), hash_function_1)

    #nonduplicate array
    nonDupArray = DynamicArray()

    #iterates through the given array
    for x in range(da.length()):
        #appends items that are not duplicates
        if(map.contains_key(da[x])):
            pass
        else:
            nonDupArray.append(da[x])

        #puts the items in the hash table
        map.put2(da[x],1)

    #final array
    newArray = DynamicArray()

    #sets the mode to the first array element
    max = map.get(nonDupArray[0])

    #iterates through the nonduplicate array
    for x in range(nonDupArray.length()):
        #gets the value from the hash table
        freq = map.get(nonDupArray[x])

        #checks if the value is greater than the mode
        if max <= freq:
            #if it's greater than the mode, it clears the array
            if(max < freq):
                newArray = DynamicArray()
            max = freq
            
            #appends the item that's the mode to the list
            newArray.append(nonDupArray[x])

    return newArray, max

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
        m.resize_table(capacity)
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
    m = HashMap(53, hash_function_1)
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
    '''
    '''
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())
    m.resize_table(1)
    print(m.get_keys_and_values())
    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())
    '''
    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", 
"Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )
    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")