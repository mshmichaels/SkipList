"""
CS 5800
Summer 2024
Homework 8/9 Test Skiplist
Miriam Michaels
"""

from skiplist import Node
from skiplist import Skiplist
import unittest
import random

skip = Skiplist()


skip.insert(10)
skip.insert(5)
skip.insert(11)
skip.insert(13)
skip.insert(7)
skip.insert(7)

skip.print_skiplist()
print(skip.in_skiplist(7))
print(f"Skiplist levels: {skip.levels}")
skip.delete(7)
skip.delete(7)
skip.delete(5)
skip.delete(13)
skip.delete(11)
skip.delete(10)

skip.print_skiplist()
print(f"Skiplist levels: {skip.levels}")

print()
print("-------------------------")
print(skip.in_skiplist(1))
skip.insert(10)
skip.insert(5)
skip.insert(11)
skip.insert(13)
skip.insert(7)
skip.insert(7)
skip.print_skiplist()


class testSkipList(unittest.TestCase):
    """
    Tests inserting and deleting a random set of numbers to a skiplist.
    """

    def test_skiplist(self):
        test = Skiplist()
        testsize = 10
        test_values = []

        while len(test_values) < testsize:
            value = random.randint(-100, 200)
            if value not in test_values:
                test.insert(value)
                test_values.append(value)

        # testing that all items have, in fact, been added to the skiplist
        self.assertEqual(test.size, testsize)
        for each in test_values:
            self.assertTrue(test.in_skiplist(each))

        # testing the order of the values in the skiplist
        node = test.sentinel.next
        while node.next.data != None:
            self.assertTrue(node.next.data >= node.data)
            node = node.next

        current_size = testsize - 1
        for each in test_values:
            test.delete(each)
            self.assertFalse(test.in_skiplist(each))
            self.assertEqual(current_size, test.size)

            current_size -= 1


if __name__ == "__main__":
    unittest.main()
