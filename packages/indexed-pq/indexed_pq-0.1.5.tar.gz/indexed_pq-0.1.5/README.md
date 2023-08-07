# indexed priority queue implemented with a python list

Three classes are implemented, namely, 
indexed min heap, indexed max heap and indexed median heap and the corresponding class names are
min_ipqa, max_ipqa, median_ipqa respectively.


an element of arbitrary index can be removed with pop_using_input_index in O(log(N))

``` python
my_min_ippa = min_ipqa()
my_min_ippa.insert(0, 1)
my_min_ippa.insert(1, 3)
my_min_ippa.insert(2, -3)
my_min_ippa.insert(3, -5)
my_min_ippa.insert(4, 5)
print('arbitrary at index 2 popped with value', my_min_ippa.pop_using_input_index(2))

while my_min_ippa.len > 0:
    print(my_min_ippa.poptop())

```
results will be
```
arbitrary at index 2 popped with value (2, -3)
(3, -5)
(0, 1)
(1, 3)
(4, 5)

```

Note that the tuple is (index, value)
and the heap is popping by ordering the value instead of the index

## Median heap
Here is a step by step examples showing the internals of the index median priority queue.
```python
my_median_ipqa = median_ipqa()
e = [1, 2, 3, 4, 2, 3, 6, 8, 4, 5]
d = 3
for i, val in enumerate(e):
    my_median_ipqa.insert(i, val)
    print(my_median_ipqa)
    print(my_median_ipqa.get_median())
```

``` 
maxheap
heaparray: [1]
heapindex: [0]
index2heap: {0: 0}
len: 1
minheap
heaparray: []
heapindex: []
index2heap: {}
len: 0
1
maxheap
heaparray: [1]
heapindex: [0]
index2heap: {0: 0}
len: 1
minheap
heaparray: [2]
heapindex: [1]
index2heap: {1: 0}
len: 1
1.5
maxheap
heaparray: [2, 1]
heapindex: [1, 0]
index2heap: {0: 1, 1: 0}
len: 2
minheap
heaparray: [3]
heapindex: [2]
index2heap: {2: 0}
len: 1
2
maxheap
heaparray: [2, 1]
heapindex: [1, 0]
index2heap: {0: 1, 1: 0}
len: 2
minheap
heaparray: [3, 4]
heapindex: [2, 3]
index2heap: {2: 0, 3: 1}
len: 2
2.5
maxheap
heaparray: [2, 1, 2]
heapindex: [1, 0, 4]
index2heap: {0: 1, 1: 0, 4: 2}
len: 3
minheap
heaparray: [3, 4]
heapindex: [2, 3]
index2heap: {2: 0, 3: 1}
len: 2
2
maxheap
heaparray: [2, 1, 2]
heapindex: [1, 0, 4]
index2heap: {0: 1, 1: 0, 4: 2}
len: 3
minheap
heaparray: [3, 4, 3]
heapindex: [2, 3, 5]
index2heap: {2: 0, 3: 1, 5: 2}
len: 3
2.5
maxheap
heaparray: [3, 2, 2, 1]
heapindex: [2, 1, 4, 0]
index2heap: {0: 3, 1: 1, 4: 2, 2: 0}
len: 4
minheap
heaparray: [3, 4, 6]
heapindex: [5, 3, 6]
index2heap: {3: 1, 5: 0, 6: 2}
len: 3
3
maxheap
heaparray: [3, 2, 2, 1]
heapindex: [2, 1, 4, 0]
index2heap: {0: 3, 1: 1, 4: 2, 2: 0}
len: 4
minheap
heaparray: [3, 4, 6, 8]
heapindex: [5, 3, 6, 7]
index2heap: {3: 1, 5: 0, 6: 2, 7: 3}
len: 4
3.0
maxheap
heaparray: [3, 3, 2, 1, 2]
heapindex: [2, 5, 4, 0, 1]
index2heap: {0: 3, 1: 4, 4: 2, 2: 0, 5: 1}
len: 5
minheap
heaparray: [4, 4, 6, 8]
heapindex: [8, 3, 6, 7]
index2heap: {3: 1, 6: 2, 7: 3, 8: 0}
len: 4
3
maxheap
heaparray: [3, 3, 2, 1, 2]
heapindex: [2, 5, 4, 0, 1]
index2heap: {0: 3, 1: 4, 4: 2, 2: 0, 5: 1}
len: 5
minheap
heaparray: [4, 4, 6, 8, 5]
heapindex: [8, 3, 6, 7, 9]
index2heap: {3: 1, 6: 2, 7: 3, 8: 0, 9: 4}
len: 5
3.5
```