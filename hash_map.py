# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def _get_index(self, key):
        """
        Gets the hash value (index) where the key should be located in the hash table
        Args:
            key: the value of the key to hash
        Return:
            The hash value (index) where the key should be located in the hash table
        """
        return self._hash_function(key) % self.capacity

    def _get_node(self, key):
        """
        Checks the hash table for the key and returns the node with that key.
        If the key is not in the table, returns None.
        Args:
            key: the value of the key to look for
        Return:
            The LinkedList node with the right key, or None if the key was not found
        """

        index = self._hash_function(key) % self.capacity  # Get the index by hashing the key
        node = self._buckets[index].contains(key)  # Get the node with the key (if it exists)
        return node

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """

        for i in range(self.capacity):
            self._buckets[i].head = None    # Empty out the LinkedList in each bucket
            self._buckets[i].size = 0
        self.size = 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """

        node = self._get_node(key)  # Get the node with the key (if it exists)

        if node is None:
            return None
        else:
            return node.value

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """

        temp = HashMap(capacity, self._hash_function)   # Temporary hash map to store new values

        for index in range(self.capacity):
            if self._buckets[index].head is not None:
                node = self._buckets[index].head
                while node is not None:
                    temp.put(node.key, node.value)      # Iterate over the values and re-hash them into the temp table
                    node = node.next

        self._buckets = temp._buckets                   # Update the hash map to use the new buckets
        self.capacity = capacity

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """

        node = self._get_node(key)  # Get the node with the key (if it exists)

        if node is None:
            index = self._get_index(key)
            self._buckets[index].add_front(key, value)      # Key was not found (add it to the front of the list)
            self.size += 1
        else:
            node.value = value                              # Key was found (update the value)

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """

        node = self._get_node(key)  # Check to see if the key is in the table
        if node is None:            # Key is not in the table (do nothing)
            return

        index = self._get_index(key)        # Get the index for the LinkedList
        node = self._buckets[index].head    # Start at the head of the LinkedList

        if node.key == key:                     # Handle the case where key is at the head
            self._buckets[index].head = node.next

        else:
            previous = node
            current = node.next
            while current.key != key:           # Find the link with the right key
                previous = current
                current = current.next
            previous.next = current.next        # Cut the link out of the list

        self.size -= 1

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """

        index = self._hash_function(key) % self.capacity
        li = self._buckets[index]
        if li.contains(key) is not None:
            return True
        return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """

        # If size is 0 or 1, we can skip traversing the hash map and save some time
        if self.size == 0 or self.size == 1:
            return self.capacity - self.size

        # Otherwise, we need to traverse the hash map and count empty buckets
        count = 0
        for i in range(self.capacity):
            if self._buckets[i].head is None:
                count += 1

        return count

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return self.size / self.capacity

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out


if __name__ == '__main__':
    # h1 = HashMap(30, hash_function_1)
    # h1.put('key1', 'value1')
    # print(h1)
    # h1.clear()

    print('function 1')
    print('eat', hash_function_1('eat'))
    print('ate', hash_function_1('ate'))

    print('function 2')
    print('eat', hash_function_2('eat'))
    print('ate', hash_function_2('ate'))
