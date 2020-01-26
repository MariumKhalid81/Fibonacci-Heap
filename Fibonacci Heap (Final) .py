
# coding: utf-8

# In[32]:


class FibonacciHeap:
    class Node:
        def __init__(self, value):            
            self.value = value
            self.parent = None        
            self.child = None
            self.left = None
            self.right = None
            self.deg = 0
            self.mark = False
    root_list =  None    
    min_node = None
    total_num_elements = 0
    # Iterate through the node list
    def iterate(self, head = None):
        if head is None:
            head = self.root_list
        current = head
        while True:
            yield current
            if current is None:
                break
            current = current.right
            if current == head:
                break
    def find_minimum(self):
        if self.min_node is None:
            raise ValueError('Fibonacci heap is Empty')
        return self.min_node.value
    def insert(self, value):
        node = self.Node(value)
        node.left = node.right = node
        self.meld_into_root_list(node)
        if self.min_node is not None:
            if self.min_node.value > node.value:
                self.min_node = node
        else:
            self.min_node = node
        self.total_num_elements += 1
        return node
    def extract_minimum(self):
        m = self.min_node
        if m is None:
            raise ValueError('Fibonacci heap is empty, cannot extract mininum!')
        if m.child is not None:
            children = [x for x in self.iterate(m.child)]
            for i in range(0, len(children)):
                self.meld_into_root_list(children[i])
                children[i].parent = None
        self.remove_from_root_list(m)
        self.total_num_elements -= 1
        self.consolidate()
        if m == m.right:
            self.min_node = None
            self.root_list = None
        else:
            self.min_node = self.find_min_node()
        return m.value
    def decrease_key(self, node, v):
        if v >= node.value:
            raise ValueError("Cannot decrease key with a value greater than what it already is.")
        node.value = v
        p = node.parent
        if p is not None and node.value < p.value:
            self.cut(node, p)
            self.cascading_cut(p)
        if node.value < self.min_node.value:
            self.min_node = node
        return
    def delete(self, node):
        self.decrease_key(node, -1)
        self.extract_minimum()
    def merge(self, fh):
        if fh.total_num_elements == 0:
            return
        if fh.min_node.value < self.min_node.value:
            self.min_node = fh.min_node
        self.total_num_elements += fh.total_num_elements
        last = fh.root_list.left
        fh.root_list.left = self.root_list.left
        self.root_list.left.right = fh.root_list
        self.root_list.left = last
        self.root_list.left.right = self.root_list
    def cut(self, node, parent):
        self.remove_from_child_list(parent, node)
        parent.deg -= 1
        self.meld_into_root_list(node)
        node.parent = None
        node.mark = False

    def cascading_cut(self, node):
        p = node.parent
        if p is not None:
            if p.mark is False:
                p.mark = True
            else:
                self.cut(node, p)
                self.cascading_cut(p)

    # Merge a node with the doubly linked root list by adding it to second position in the list
    def meld_into_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    # Deletes a node from the doubly linked root list.
    def remove_from_root_list(self, node):
        if self.root_list is None:
            raise ValueError('Fibonacci heap is empty, there is no node to remove!')
        if self.root_list == node:
            # Check if there's only one element in the list
            if self.root_list == self.root_list.right:
                self.root_list = None
                return
            else:
                self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left
        return

    # Removes a node from the doubly linked child list
    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left
    
    # Consolidates trees so that no root has same rank.
    def consolidate(self):
        if self.root_list is None:
            return
        ranks_mapping = [None] * self.total_num_elements
        nodes = [x for x in self.iterate(self.root_list)]
        for node in nodes:
            degree = node.deg
            while ranks_mapping[degree] != None:
                other = ranks_mapping[degree]
                if node.value > other.value:
                    node, other = other, node
                self.merge_nodes(node, other)
                ranks_mapping[degree] = None
                degree += 1
            ranks_mapping[degree] = node
        return
    def merge_nodes(self, node, other):
        self.remove_from_root_list(other)
        other.left = other.right = other
        # Adding other node to child list of the frst one.
        self.merge_with_child_list(node, other)
        node.deg += 1
        other.parent = node
        other.mark = False
        return
    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node
    def find_min_node(self):
        if self.root_list is None:
            return None
        else:
            min = self.root_list
            for x in self.iterate(self.root_list):
                if x.value < min.value:
                    min = x
            return min
    def print(self, head = None):
        if self.root_list is not None:
            for heap in self.iterate():
                print('---')
                self.print_tree(heap)
                print()
            print('---')
    def print_tree(self, node):
        if node is None:
            return
        print(node.value, end=' ')
        if node.child is not None:
            print()
            for child in self.iterate(node.child):
                self.print_tree(child)
    def find_node_greater_than(self, value):
        if self.root_list is not None:
            for heap in self.iterate():
                result = self.find_child_greater_than(heap, value)
                if result != None:
                    return result
        raise ValueError(f'There is no element in the heap that is greater than {value}.')
    def find_child_greater_than(self, node, value):
        if node is None:
            return None
        elif node.value > value:
            return node
        if node.child is not None:
            for child in self.iterate(node.child):
                result = self.find_child_greater_than(child, value)
                if result is not None:
                    return result
        return None
#drivercode
print("......................FIBONACCI HEAP IMPLEMENTATION..................\n\n")
f = FibonacciHeap()
print("Constructing heap... ")
print("Inserting elements... ", end='')
f.insert(2)
f.insert(3)
to_delete = f.insert(4)
to_decrease = f.insert(5)
f.insert(1)
print("Done.")
print("Printing heap...")
f.print()
print("Min: ", end='')
print(f.find_minimum())
print("Min (linear): ", end='')
print(f.find_min_node().value)
print("Deleting minimum: ")
print(f.extract_minimum())
print("Done!")
print("Printing heap...")
f.print()
print("Min: ", end='')
print(f.find_minimum())
print("Min: ", end='')
print(f.find_min_node().value)
print(f"Decrease {to_decrease.value} to 1: ")
f.decrease_key(to_decrease, 1)
f.print()
print("Min: ", end='')
print(f.find_minimum())
print(f"Delete {to_delete.value}: ")
f.delete(to_delete)
f.print()
f2 = FibonacciHeap()
f2.insert(60)
f2.insert(32)
print("Heap 2: ")
f2.print()
print("Merging:")
f.merge(f2)
f.print()    


