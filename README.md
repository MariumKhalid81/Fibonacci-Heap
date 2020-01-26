# Fibonacci-Heap
Data Structure Project on Fibonacci Heap
Functions used in this Fibonacci heap are as follows.
Iterate(value)
Insert(value
findmin()
extractmin()
Printheap()
printTree()
merge()
decreasekey()


Iterate():
This function Iterate through the node list.

Insert(value):
It takes one argument which is value and Insert works by creating a new heap with one element and doing merge. This takes constant time, and the potential  increases by one, because the number of trees increases. The amortized cost is thus still constant. 

findmin():
this function find the minimum node from the heap.

merge():
this function merging two heaps is implemented simply by concatenating the lists of tree roots of the two heaps.  This can be done in constant time and the potential does not change, leading again to constant amortized time.

extractrmin():
This function extract the minimum value and the amortized running time of this phase is O(d) = O(log n).

decrease key():
This function decreases the key by the node value.

 printheap():
This function helps to print the completre heap after inserting or performing other operations.







Group Members
Marium Khalid  (18B-012-SE)
Mohammad Moin (18B-099-SE)
