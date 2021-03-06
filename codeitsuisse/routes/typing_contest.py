import logging
import json
import distance


from flask import request, jsonify;

from codeitsuisse import app;

import sys # Library for INT_MAX 
from collections import Counter, defaultdict

logger = logging.getLogger(__name__)

@app.route('/typing-contest', methods=['POST'])
def typing_contest():
    data = request.get_json()

    counter = Counter(data)
    # print(counter)
    # print(counter.keys())
    keys = list(counter.keys())
    # print(keys)
    # print("\n\n\n")

    adj = [[0 for _ in range(len(keys))] for _ in range(len(keys))]
    for i in range(len(keys)):
        for j in range(len(keys)):
            adj[i][j] = distance.hamming(keys[i], keys[j])
     
    # print(adj)
    # print(keys)
    # build adj matrix

    g = Graph(len(keys)) 
    g.graph = adj

    mst = g.primMST()

    res = {}
    res["cost"] = len(data[0]) + len(data) - 1 + sum([e[2] for e in mst])
    
    d = defaultdict(list)
    visited = [0 for _ in range(len(keys))]

    # print(mst)
    for m in mst:
        d[m[0]].append(m[1])
        d[m[1]].append(m[0])
    
    steps = []
    steps.append({"type" : "INPUT", "value" : keys[0]})
    
    print(len(adj))
    print(len(data))

    stack = [(0,i) for i in d[0]]
    while not all(visited):
        new_stack = []
        for node in stack:
            # print(stack)
            steps.append({"type": 'COPY', "value": keys[node[0]]})
            steps.append({"type": 'TRANSFORM', "value": keys[node[1]]})
            visited[node[0]] = 1
            if not visited[node[1]]:
                visited[node[1]] = 1
                arr = []
                for nod in d[node[1]]:
                    if not visited[nod]:
                        new_stack.append((node[1],nod))
        stack = new_stack
        # print(new_stack, "\n\n")

    for k,v in counter.items():
        for _ in range(v-1):
            steps.append({"type": 'COPY', "value": k})

    # print(steps)
    res["steps"] = steps
    return jsonify(res)

    
class Graph(): 
  
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = [[0 for column in range(vertices)]  
                    for row in range(vertices)] 
  
    # A utility function to find the vertex with  
    # minimum distance value, from the set of vertices  
    # not yet included in shortest path tree 
    def minKey(self, key, mstSet): 
  
        # Initilaize min value 
        min = sys.maxsize 
  
        for v in range(self.V): 
            if key[v] < min and mstSet[v] == False: 
                min = key[v] 
                min_index = v 
  
        return min_index 
  
    # Function to construct and print MST for a graph  
    # represented using adjacency matrix representation 
    def primMST(self): 
  
        # Key values used to pick minimum weight edge in cut 
        key = [sys.maxsize] * self.V 
        parent = [None] * self.V # Array to store constructed MST 
        # Make key 0 so that this vertex is picked as first vertex 
        key[0] = 0 
        mstSet = [False] * self.V 
  
        parent[0] = -1 # First node is always the root of 
  
        for cout in range(self.V): 
  
            # Pick the minimum distance vertex from  
            # the set of vertices not yet processed.  
            # u is always equal to src in first iteration 
            u = self.minKey(key, mstSet) 
  
            # Put the minimum distance vertex in  
            # the shortest path tree 
            mstSet[u] = True
  
            # Update dist value of the adjacent vertices  
            # of the picked vertex only if the current  
            # distance is greater than new distance and 
            # the vertex in not in the shotest path tree 
            for v in range(self.V): 
                # graph[u][v] is non zero only for adjacent vertices of m 
                # mstSet[v] is false for vertices not yet included in MST 
                # Update the key only if graph[u][v] is smaller than key[v] 
                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]: 
                        key[v] = self.graph[u][v] 
                        parent[v] = u 
  
        # self.printMST(parent)
        return [(parent[i], i, self.graph[i][parent[i]]) for i in range(1, self.V)]
  

    # A utility function to print the constructed MST stored in parent[] 
#     def printMST(self, parent): 
#         print("Edge \tWeight")
#         for i in range(1, self.V): 
#             print(parent[i], "-", i, "\t", self.graph[i][ parent[i] ])
  

# g = Graph(5) 
# g.graph = [ [0, 2, 0, 6, 0], 
#             [2, 0, 3, 8, 5], 
#             [0, 3, 0, 0, 7], 
#             [6, 8, 0, 0, 9], 
#             [0, 5, 7, 9, 0]]
# g.primMST()