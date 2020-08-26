# word_count.py
# ===================================================
# Implement a word counter that counts the number of
# occurrences of all the words in a file. The word
# counter will return the top X words, as indicated
# by the user.
# ===================================================

import re
from hash_map import HashMap


class Heap:
    """Implements a heap with sorting functions to help sort word count data"""

    def __init__(self):
        """Creates an empty heap"""
        self.heap = []

    def insert(self, data):
        """Adds word data to the heap.
        Args:
            data: A tuple containing a word and the associated count e.g.: (butterfly, 1), (questions, 4)
        """
        self.heap.append(data)          # Add the value to the end of the heap
        index = len(self.heap) - 1      # Get the index for the newly added element

        if index > 0:                           # Make sure we're not at the top of the heap already
            parent_index = ((index - 1) // 2)   # Get the parent index for the newly added element

            # If word count is greater, swap the values (this puts less frequent words at the top of the heap)
            while index > 0 and self.heap[index][1] < self.heap[parent_index][1]:

                temp = self.heap[index]
                self.heap[index] = self.heap[parent_index]
                self.heap[parent_index] = temp

                index = parent_index
                parent_index = ((index - 1) // 2)

    def sort(self):
        """Sorts the heap by the number of word occurrences, descending"""

        # Handle empty heaps, heaps with one element
        if len(self.heap) <= 1:
            return

        # Index that separates sorted from unsorted values (Unsorted values before k, sorted values start at k)
        k = len(self.heap) - 1

        while k > 0:

            # Value at the top of the heap moves to the sorted section
            temp = self.heap[0]
            self.heap[0] = self.heap[k]
            self.heap[k] = temp

            # Value that used to be at the end percolates down to its proper place (ignoring everything past k)
            index = 0
            l_index = 1
            r_index = 2

            # Stop if there are no eligible children to switch with
            while ((l_index < k and self.heap[l_index][1] < self.heap[index][1]) or     # Left child < parent
                   (r_index < k and self.heap[r_index][1] < self.heap[index][1])):      # Right child < parent

                # Two eligible children, right child is smaller (switch parent with right child)
                if (r_index < k and self.heap[r_index][1] < self.heap[l_index][1] and
                        self.heap[r_index][1] < self.heap[index][1]):
                    temp = self.heap[index]
                    self.heap[index] = self.heap[r_index]
                    self.heap[r_index] = temp

                    index = r_index
                    l_index = index * 2 + 1
                    r_index = index * 2 + 2

                # Otherwise, switch parent with left child
                else:
                    temp = self.heap[index]
                    self.heap[index] = self.heap[l_index]
                    self.heap[l_index] = temp

                    index = l_index
                    l_index = index * 2 + 1
                    r_index = index * 2 + 2

            k -= 1  # Move the sort index


"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard we can test against, so don't
modify it for your assignment submission.
"""
rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    """
    This is a hash function that can be used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500, hash_function_2)

    # This block of code will read a file one word as a time and
    # put the word in `w`. It should be left as starter code.
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                w = w.lower()
                count = ht.get(w)
                if count is None:
                    ht.put(w, 1)            # Word is not in the hash map; add it
                else:
                    ht.put(w, count + 1)    # Word is in the hash map; increment the count

    heap = Heap()   # Create a heap to do the sorting

    for i in range(ht.capacity):
        node = ht._buckets[i].head
        while node is not None:
            t = (node.key, node.value)
            heap.insert(t)                  # Add each tuple to the heap
            node = node.next

    heap.sort()     # Sort by word count, descending

    if number <= len(heap.heap):
        return heap.heap[0:number]
    else:
        return heap.heap     # Handles the case where the user requests too many words

print(top_words("alice.txt",10))
