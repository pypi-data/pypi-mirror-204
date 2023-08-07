# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 10:35:32 2023

@author: 
"""

class min_ipqa():
    '''
    sample test code
# my_min_ippa = min_ipqa()
# my_min_ippa.insert(0, 1)
# my_min_ippa.insert(1, 3)
# my_min_ippa.insert(2, -3)
# my_min_ippa.insert(3, -5)
# my_min_ippa.insert(4, 5)
# print('arbitrary at index 2 popped with value', my_min_ippa.pop_using_input_index(2))

# while my_min_ippa.len > 0:
#     print(my_min_ippa.poptop())
'''
    def __init__(self):
        self.heaparray = [] # internal heap representation
        self.heapindex = [] # from index in internal heap to find its original index in the input array
        self.index2heap = {} # given and unique index in input array, find the associated index in heap array
        self.len = 0
        # can add a value to heap index location look up,
    def __repr__(self):
        return (f"heaparray: {self.heaparray}" + '\n' +
                f"heapindex: {self.heapindex}"+ '\n' +
                f"index2heap: {self.index2heap}" + '\n' +
                f"len: {self.len}")
        
    def insert(self, index, value):
        
        self.heaparray.append(value)
        self.heapindex.append(index)
        self.index2heap[index] = self.len
        self.len += 1
        self.swim(self.len-1)
    def swap(self, i_heap, i_heap_to_swap_with):
        i_index = self.heapindex[i_heap]
        i_index_to_swap_with = self.heapindex[i_heap_to_swap_with]
        self.heaparray[i_heap], self.heaparray[i_heap_to_swap_with] = self.heaparray[i_heap_to_swap_with], self.heaparray[i_heap]
        self.heapindex[i_heap], self.heapindex[i_heap_to_swap_with] = self.heapindex[i_heap_to_swap_with], self.heapindex[i_heap]
        
        self.index2heap[i_index], self.index2heap[i_index_to_swap_with] = self.index2heap[i_index_to_swap_with], self.index2heap[i_index]
        assert i_index == self.heapindex[self.index2heap[i_index]]
        assert i_index_to_swap_with == self.heapindex[self.index2heap[i_index_to_swap_with]]
    def swim(self, i_heap):
        while ((i_heap >0) and (self.heaparray[i_heap] < self.heaparray[(i_heap+1)//2 - 1])):
            i_heap_to_swap_with = (i_heap+1)//2 - 1
            self.swap(i_heap, i_heap_to_swap_with)
            i_heap = i_heap_to_swap_with
        return i_heap
    def get_smallest_child_index(self, i_heap):
        if i_heap * 2 + 1 < self.len - 1:
            i1 = i_heap * 2 + 1
            i2 = (i_heap+1) * 2
            if self.heaparray[i1] < self.heaparray[i2]:
                return i1
            else:
                return i2
        elif i_heap * 2 + 1 < self.len:    
            return i_heap * 2 + 1 # only 1 child
        else:
            return None
    def has_child(self, i_heap):
        return i_heap * 2 + 1 < self.len
    def swimdown(self, i_heap):
        smallest_child_index = self.get_smallest_child_index(i_heap)
        while smallest_child_index is not None:
            if self.heaparray[i_heap] >  self.heaparray[smallest_child_index]:
                i_heap_to_swap_with = smallest_child_index
                self.swap(i_heap, i_heap_to_swap_with)
                i_heap = i_heap_to_swap_with
                smallest_child_index = self.get_smallest_child_index(i_heap)
            else:
                break
        return i_heap
    def remove_last(self):
        self.index2heap.pop(self.heapindex[self.len-1])
        
        self.len -=1
        return self.heapindex.pop(-1), self.heaparray.pop(-1)
    def poptop(self):
        self.swap(0, self.len-1)
        top = self.remove_last()
        if self.len > 0:
            self.swimdown(0)
        return top
    def pop_using_input_index(self, input_index):
        i_heap_to_remove = self.index2heap[input_index]
        if i_heap_to_remove == self.len-1 :
            return self.remove_last()
        self.swap(i_heap_to_remove, self.len-1)
        to_remove = self.remove_last()
        #i_heap_to_swim = i_heap_to_remove
        self.swimdown(i_heap_to_remove)
        self.swim(i_heap_to_remove)
        return to_remove
            


class max_ipqa():
    '''
    sample test code
    # my_max_ippa = max_ipqa()
    # my_max_ippa.insert(0, 1)
    # my_max_ippa.insert(1, 3)
    # my_max_ippa.insert(2, -3)
    # my_max_ippa.insert(3, -5)
    # my_max_ippa.insert(4, 5)
    # print('arbitrary at index 2 popped with value', my_max_ippa.pop_using_input_index(2))
    # while my_max_ippa.len > 0:
    #     print(my_max_ippa.poptop())
    '''
    def __init__(self):
        self.heaparray = [] # internal heap representation
        self.heapindex = [] # from index in internal heap to find its original index in the input array
        self.index2heap = {} # given and unique index in input array, find the associated index in heap array
        self.len = 0
        # can add a value to heap index location look up,
    def __repr__(self):
        return (f"heaparray: {self.heaparray}" + '\n' +
                f"heapindex: {self.heapindex}"+ '\n' +
                f"index2heap: {self.index2heap}" + '\n' +
                f"len: {self.len}")
        
    def insert(self, index, value):
        
        self.heaparray.append(value)
        self.heapindex.append(index)
        self.index2heap[index] = self.len
        self.len += 1
        self.swim(self.len-1)
    def swap(self, i_heap, i_heap_to_swap_with):
        i_index = self.heapindex[i_heap]
        i_index_to_swap_with = self.heapindex[i_heap_to_swap_with]
        self.heaparray[i_heap], self.heaparray[i_heap_to_swap_with] = self.heaparray[i_heap_to_swap_with], self.heaparray[i_heap]
        self.heapindex[i_heap], self.heapindex[i_heap_to_swap_with] = self.heapindex[i_heap_to_swap_with], self.heapindex[i_heap]
        
        self.index2heap[i_index], self.index2heap[i_index_to_swap_with] = self.index2heap[i_index_to_swap_with], self.index2heap[i_index]
        assert i_index == self.heapindex[self.index2heap[i_index]]
        assert i_index_to_swap_with == self.heapindex[self.index2heap[i_index_to_swap_with]]
    def swim(self, i_heap):
        while ((i_heap >0) and (self.heaparray[i_heap] > self.heaparray[(i_heap+1)//2 - 1])):
            i_heap_to_swap_with = (i_heap+1)//2 - 1
            self.swap(i_heap, i_heap_to_swap_with)
            i_heap = i_heap_to_swap_with
        return i_heap
    def get_largest_child_index(self, i_heap):
        if i_heap * 2 + 1 < self.len - 1:
            i1 = i_heap * 2 + 1
            i2 = (i_heap+1) * 2
            if self.heaparray[i1] > self.heaparray[i2]:
                return i1
            else:
                return i2
        elif i_heap * 2 + 1 < self.len:    
            return i_heap * 2 + 1 # only 1 child
        else:
            return None
    def has_child(self, i_heap):
        return i_heap * 2 + 1 < self.len
    def swimdown(self, i_heap):
        largest_child_index = self.get_largest_child_index(i_heap)
        while largest_child_index is not None:
            if self.heaparray[i_heap] <  self.heaparray[largest_child_index]:
                i_heap_to_swap_with = largest_child_index
                self.swap(i_heap, i_heap_to_swap_with)
                i_heap = i_heap_to_swap_with
                largest_child_index = self.get_largest_child_index(i_heap)
            else:
                break
        return i_heap
    def remove_last(self):
        self.index2heap.pop(self.heapindex[self.len-1])
        
        self.len -=1
        return self.heapindex.pop(-1), self.heaparray.pop(-1)
    def poptop(self):
        self.swap(0, self.len-1)
        top = self.remove_last()
        if self.len > 0:
            self.swimdown(0)
        return top
    def pop_using_input_index(self, input_index):
        i_heap_to_remove = self.index2heap[input_index]
        if i_heap_to_remove == self.len-1 :
            return self.remove_last()
        self.swap(i_heap_to_remove, self.len-1)
        to_remove = self.remove_last()
        #i_heap_to_swim = i_heap_to_remove
        self.swimdown(i_heap_to_remove)
        self.swim(i_heap_to_remove)
        return to_remove



class median_ipqa():
    """ test meidan priority queue
    my_median_ipqa = median_ipqa()
    e = [1, 2, 3, 4, 2, 3, 6, 8, 4, 5]
    d = 3
    for i, val in enumerate(e):
        my_median_ipqa.insert(i, val)
        print(my_median_ipqa)
        print(my_median_ipqa.get_median())
    """
    def __init__(self):
        self.min_heap = min_ipqa()
        self.max_heap = max_ipqa()
    def get_median(self):
        if self.max_heap.len == 0:
            return None
        if self.min_heap.len < self.max_heap.len:
            return self.max_heap.heaparray[0]
        else:
            return (self.max_heap.heaparray[0] + self.min_heap.heaparray[0]) / 2
    def get_2_times_median(self):
        if self.max_heap.len == 0:
            return None
        if self.min_heap.len < self.max_heap.len:
            return self.max_heap.heaparray[0] * 2
        else:
            return (self.max_heap.heaparray[0] + self.min_heap.heaparray[0])
    @property
    def len(self):
        return self.min_heap.len + self.max_heap.len
        
    def insert(self, index, value):
        
        median = self.get_median()
        if median is None:
            self.max_heap.insert(index,value)
        else:
            if value <= median:
                self.max_heap.insert(index, value)
            else:
                self.min_heap.insert(index, value)
            self.rebalance()
    def rebalance(self):
        if self.min_heap.len > self.max_heap.len:
            index_popped, value_popped = self.min_heap.poptop()
            self.max_heap.insert(index_popped, value_popped)
        if self.min_heap.len+1 < self.max_heap.len:
            index_popped, value_popped = self.max_heap.poptop()
            self.min_heap.insert(index_popped, value_popped)
    def pop_by_index(self, index):
        
        if index in self.max_heap.index2heap:
            to_return = self.max_heap.pop_using_input_index(index)
        else:
            to_return = self.min_heap.pop_using_input_index(index)
        self.rebalance()
        return to_return
    def __repr__(self):
        
        return "maxheap\n"+self.max_heap.__repr__() + '\nminheap\n' + self.min_heap.__repr__()