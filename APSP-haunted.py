import copy
import networkx as nx
import numpy as np
import random

numVertices = 7
maxHauntedGalaxies = 6
MAX = 9999999


#use to print distance matrix, must specify number of haunted galaxies
def printGraph(graph, numHauntedGalaxies):
    for i in range(numVertices):
        for j in range(numVertices):
            if graph[i][j][numHauntedGalaxies] == MAX:
                print("X", end=' ')
            else:
                print(graph[i][j][numHauntedGalaxies], end=' ')
        print()
    print()

# use to print graph before it gets expanded
def printGraph1D(graph):
    for i in range(numVertices):
        for j in range(numVertices):
            if graph[i][j] == MAX:
                print("X", end=' ')
            else:
                print(graph[i][j], end=' ')
        print()
    print()

# computes all pairs shortest path without the haunted galaxies
def allPairsShortestPath(graph, haunted):
    dist = copy.deepcopy(graph)

    #do not consider haunted galaxies
    for i in range(len(haunted)):
        if haunted[i] == 1:
            dist[i] = [MAX]*len(haunted)
            for j in range(len(haunted)):
                dist[j][i] = MAX
                

    for k in range(numVertices):
        for i in range(numVertices):
            for j in range(numVertices):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# DEPRICATED
def addHauntedGalaxiesBack(originalGraph, nonHauntedGraph):
    ans = copy.deepcopy(nonHauntedGraph)
    for i in range(numVertices):
        for j in range(numVertices):
            ans[i][j] = min(nonHauntedGraph[i][j], originalGraph[i][j])
    return ans

# expands the non haunted graph where the first index is the haunted graph and the next ones are the original graphs
# prepares the graph for the second APSP
def addDimensionToGraph(graph, originalGraph):
    for i in range(numVertices):
        for j in range(numVertices):
            arr = [originalGraph[i][j]]*(maxHauntedGalaxies+1)
            arr[0] = graph[i][j]
            graph[i][j] = arr
    return graph

# finds the shortest path for each level corresponding to how many haunted galaxies are allowed
def findAstroHauntedPaths(graph):
    dist = copy.deepcopy(graph)
    for m in range(1, maxHauntedGalaxies+1):
        for k in range(numVertices):
            for i in range(numVertices):
                for j in range(numVertices):
                    dist[i][j][m] = min(dist[i][j][m], dist[i][k][m-1] + dist[k][j][1])
    return dist

def main():
    #REMEMBER to change numvertices and maxhaunted at the top of the file when testing different graphs

    #haunted = [0,1,1,0]
    #graph = [
    #    [0, 5, MAX, 10],
    #    [MAX, 0, 3, MAX],
    #    [MAX, MAX, 0, 1],
    #    [MAX, MAX, MAX, 0]
    #]
    haunted = [0]*numVertices
    for i in range(1, len(haunted)-1):
        haunted[i] = random.randint(0, 1)
    graph = nx.gnm_random_graph(numVertices, random.randint(1, numVertices))
    for u,v,w in graph.edges(data=True):
        w['weight'] = np.random.randint(1,10)
    graph = nx.to_numpy_array(graph)
    graph = graph.tolist()
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if i != j and graph[i][j] == 0:
                graph[i][j] = MAX
    # graph = [
    #     [0,1,MAX,MAX,MAX,MAX,MAX],
    #     [MAX,0,1,MAX,MAX,MAX,MAX],
    #     [MAX,MAX,0,1,MAX,MAX,MAX],
    #     [MAX,MAX,MAX,0,1,MAX,MAX],
    #     [MAX,MAX,MAX,MAX,0,1,MAX],
    #     [MAX,MAX,MAX,MAX,MAX,0,1],
    #     [MAX,MAX,MAX,MAX,MAX,MAX,0]
    # ]

    original = copy.deepcopy(graph)

    nonHaunted = allPairsShortestPath(graph, haunted)

    #combined = addHauntedGalaxiesBack(original, nonHaunted)

    temp = addDimensionToGraph(nonHaunted,original)

    result = findAstroHauntedPaths(temp)
    print("0 haunted galaxies allowed")
    printGraph(result,0)
    print("1 haunted galaxy allowed")
    printGraph(result,1)
    print("2 haunted galaxies allowed")
    printGraph(result,2)
    print("3 haunted galaxies allowed")
    printGraph(result,3)
    print("4 haunted galaxy allowed")
    printGraph(result,4)
    print("5 haunted galaxies allowed")
    printGraph(result,5)
    print("6 haunted galaxies allowed")
    printGraph(result,6)

if __name__ == "__main__":
    main()