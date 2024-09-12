# SkipList
Python Skip List

Skip lists are linked list data structures that insert, search, and delete in an average of lg(n) time. This makes them efficient in terms of memory use and standard data structure operations. 

This skip list is structured with a base linked list where each number is stored. When a number is added, "levels" are added to it to a level determined by a coin flip function. The average "height" of each number stored is lg(n). When searching for a value, the list starts at the top "level" and uses the higher levels in a binary search fashion so the average search time is lg(n). This implementation is circular, with a sentinel as the start and end node of the base linked list that maintains its height to be the same as the highest level of any number in the skip list. When a value is deleted, its upper levels are also deleted. 
