import logging
import json
from collections import defaultdict 

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/generateSequence', methods=['POST'])
def dependency_manager():
    data = request.get_json()
    print(data)
    logging.info("data sent for evaluation {}".format(data))

    modules = {}
    for i,m in enumerate(data["modules"]):
        modules[m] = i

    g = Graph(len(data["modules"]))

    print("\n\n")
    print(data["dependencyPairs"])
    print(data["modules"])

    for element in data["dependencyPairs"]:
        g.addEdge(modules[element["dependee"]], 
                  modules[element["dependentOn"]])
    res,cyclic = g.topoSort()

    result = []
    for r in res:
        if cyclic[r]:
            result.append(data["modules"][r])
    
    return json.dumps(result[::-1])

  
#Class to represent a graph 
class Graph: 
    def __init__(self,vertices): 
        self.graph = defaultdict(list) #dictionary containing adjacency List 
        self.V = vertices #No. of vertices
        self.cyclic = [True for _ in range(vertices)]
  
    # function to add an edge to graph 
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
  
    # A recursive function used by topoSort 
    def topoSortUtil(self,v,start,visited,stack): 
  
        # Mark the current node as visited. 
        visited[v] = True
  
        # Recur for all the vertices adjacent to this vertex 
        for i in self.graph[v]: 

            # return to the starting point, graph is cyclic
            # no topo sort is possible
            if i == start:
                self.cyclic[i] = False
                return -1

            if visited[i] == False: 
                # apply to nodes in the tree
                res = self.topoSortUtil(i,start,visited,stack)

                # propogate the result out
                if res == -1:
                    self.cyclic[i] = False
                    return -1
  
        # Push current vertex to stack which stores result 
        stack.insert(0,v)
  
    # The function to do Topological Sort. It uses recursive  
    # topoSortUtil() 
    def topoSort(self): 
        # Mark all the vertices as not visited 
        visited = [False]*self.V 
        stack = []
  
        # Call the recursive helper function to store Topological 
        # Sort starting from all vertices one by one 
        for i in range(self.V):
            if visited[i] == False:
                res = self.topoSortUtil(i,i,visited,stack)
                if res == -1:
                    self.cyclic[i] = False

        # Print contents of the stack 
        return stack, self.cyclic
