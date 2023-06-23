# Implement the Depth-First Search algorithm on a graph.
def depthFirstSearch(graph, start):
    """
    graph: Graph represented as a dictionary
    start: Starting vertex
    """
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited

# Implement the Breadth-First Search algorithm on a graph.
from collections import deque
def bfs(graph, root):
    """
    graph: Graph represented as a dictionary
    root: Starting vertex
    """
    visited, queue = set(), deque([root])
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
    return visited
    
# Implement the quicksort sorting algorithm.
def quicksort(arr):
    """
    arr: List of elements to sort
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
