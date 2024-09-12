"""
CS 5800
Summer 2024
Homework 8/9 Skiplist
Miriam Michaels
"""

import random


class Node:
    """
    Node class defines a node for a skiplist. Each node has pointers next and
    previous, up, and down, so the skiplist can be traversed in all directions.
    Each node also contains data and its level.
    """

    def __init__(self, data: float) -> None:
        self.data = data
        self.next = None
        self.prev = None
        self.up = None
        self.down = None
        self.level = 1


class Skiplist:
    """
    Skiplist class keeps track of an instance of a skip list and has all the
    needed skiplist functions as methods. Each base linked list is doubly linked
    and circular leading to a sentinel node.
    """

    def __init__(self) -> None:
        self.sentinel = Node(None)
        self.levels = 0
        self.travel_list = []
        self.size = 0

    def insert(self, data: float) -> None:
        """
        Insert function inserts a value into the skiplist.

        Parameters:
            data -- float, data to be entered into the skiplist
        """
        self.size += 1
        new_node = Node(data)
        new_level = self.coinflip()

        # if the skip list is empty, inserts a node into it
        if self.sentinel.next == None:
            # creating right/left connections in bottom linked list
            self.sentinel.next = self.sentinel.prev = new_node
            new_node.next = new_node.prev = self.sentinel
            self.levels = new_level
            up_sentinel = self.sentinel
            up_node = new_node
            for each in range(1, new_level + 1):
                # creating higher levels for sentinel and first node
                up_sentinel = self.add_level(up_sentinel, each + 1)
                up_node = self.add_level(up_node, each + 1)

                # creating right/left connections in upper linked list
                up_sentinel.next = up_sentinel.prev = up_node
                up_node.next = up_node.prev = up_sentinel

        else:  # adding non-first nodes into the skiplist
            current = self.find_predecessor(data)

            # linking in new node to bottom level
            self.add_after(current, new_node)
            new_node.level = 1

            # adding height to the sentinel linked list if needed
            sent = self.find_top()
            while new_level > self.levels:
                sent = self.add_level(sent, sent.level + 1)
                sent.next = sent.prev = sent
                self.levels += 1

            # adding in upper nodes if needed
            if new_level > 1:
                curr_level = 2  # already added level 1
                travel_list_iterator = len(self.travel_list) - 2
                up_node = new_node

                # adds nodes in the middle of upper linked lists
                for each in range(len(self.travel_list)):
                    current = self.travel_list[travel_list_iterator]
                    if current.level == curr_level:
                        # adding a node up the list
                        up_node = self.add_level(up_node, curr_level)

                        # linking in up node to next level up
                        self.add_after(current, up_node)

                        up_node.level = curr_level
                        curr_level += 1
                    travel_list_iterator -= 1

                # deals with case where new node is taller than all other nodes
                if up_node.level < new_level:
                    # raising up sentinel node to needed height
                    sent = self.sentinel
                    while sent.level < up_node.level:
                        sent = sent.up

                    # linking sentinel node to new node
                    while up_node.level < new_level:
                        sent = sent.up
                        up_node = self.add_level(up_node, curr_level)
                        self.add_after(sent, up_node)

                        curr_level += 1

    def find_top(self) -> Node:
        """
        Finds the top of the skiplist sentinel and returns it. The sentinel node
        stored in the skiplist is at the bottom level, this traverses up through
        all the levels.
        """
        node = self.sentinel
        while node.level != self.levels:
            node = node.up
        return node

    def add_after(self, predecessor: Node, newnode: Node) -> None:
        """
        Adds one node after another in a horizontal doubly linked list.

        Parameters:
            predecessor -- Node, other node is added after this one
            newnode -- Node, is added after predecessor
        """
        newnode.next = predecessor.next
        newnode.next.prev = newnode
        newnode.prev = predecessor
        predecessor.next = newnode

    def print_skiplist(self) -> None:
        """
        Prints the skiplist level by level starting with the base linked list
        and moving up to each subsequent level.
        """
        sent = self.sentinel
        for each in range(self.levels):
            current = sent.next
            print(f"Level {each + 1}: ", end="")
            while current.data != None:
                print(f"{current.data} -> ", end="")
                current = current.next
            print("sentinel")
            # circling back to sentinel and going up a level
            sent = sent.up

    def add_level(self, node: Node, new_level: int) -> Node:
        """
        Adds a level to a node's up/down stack.

        Parameters:
            node -- Node, where level should be added
            new_level -- int, the level number of the new level
        Returns:
            up_node -- Node, at the input level
        """
        up_node = Node(node.data)
        up_node.level = new_level
        node.up = up_node
        up_node.down = node
        return up_node

    def coinflip(self) -> int:
        """
        Runs a random number generator to represent a coin flip. Adds to a
        counter until 0 is generated, then the count is returned.

        Returns:
            result -- int, the number of times the coin landed heads
        """
        result = 1
        while random.randint(0, 1) != 0:
            result += 1
        return result

    def delete(self, data: float) -> None:
        """
        Deletes a value from the skip list by finding its predecessor, and
        removing its entire stack of nodes. If the sentinel stack is now taller
        than any of the nodes, it is reduced down to the tallest node.

        Parameters:
            data -- float, the value to be removed from the skip list
        """
        node = self.find_predecessor(data).next
        if node.data == data:
            self.size -= 1
            # moves through all vertical levels, removing the node
            while node != None:
                node.prev.next = node.next
                node.next.prev = node.prev

                if node.next == node.prev:  # node is only pointing to sentinel
                    # disconnect from below
                    if node.next.level >= 2:
                        self.levels -= 1
                        node.next.down.up = None

                node = node.up
        # skiplist never goes below level 1
        self.levels = 1

    def find_predecessor(self, data: float) -> Node:
        """
        Finds the value prior to a sought after value in the skip list. Starts
        at the top of the sentinel stack and moves to the right as many times
        as possible before moving down a level. Maintains a list of nodes
        traversed that is used by the insert method.

        Parameters:
            data -- float, data to find predecessor of
        Returns:
            current -- Node, node that is prior to the sought after value
        """
        mynode = self.sentinel
        current = self.find_top()  # starts at the top of the sentinel stack
        self.travel_list = []  # empties travel list to refill it
        self.travel_list.append(current)

        found = False
        while not found:
            # traversing to the right
            if current.next.data != None and current.next.data < data:
                current = current.next
                self.travel_list.append(current)

            elif current.level > 1:  # traversing down
                current = current.down
                self.travel_list.append(current)

            else:
                found = True

        return current

    def in_skiplist(self, data: float) -> bool:
        """
        Checks whether a value is in the skiplist and returns a boolean.

        Parameters:
            data -- float, value to check for
        Returns:
            boolean -- whether the data was found in the skip list
        """
        node = self.find_predecessor(data).next
        return node.data == data
