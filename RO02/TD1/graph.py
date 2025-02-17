import numpy as np

class Edge:
    """
    Represents an edge in a graph with two endpoints (id1, id2) and a weight.
    """

    id1 = 0
    id2 = 0
    weight = 0.0

    def __init__(self, id1, id2, weight):
        """
        Initializes an edge with given node IDs and weight.
        """
        self.id1 = id1
        self.id2 = id2
        self.weight = weight
        
    def __lt__(self, other):
        """
        Defines the less than (<) operator to compare edges based on weight.
        """
        return self.weight <= other.weight

    def __eq__(self, other):
        """
        Defines equality comparison for edges.
        Two edges are considered equal if they connect the same nodes,
        regardless of order.
        """
        return self.id1 == other.id1 and self.id2 == other.id2 or self.id1 == other.id2 and self.id2 == other.id1


class Graph:
    """
    Represents a graph using an adjacency matrix.
    """

    n = 0  # Number of nodes
    nodes = np.array([])  # Array of node names
    adjacency = np.empty(0)  # Adjacency matrix

    def __init__(self, sNames):
        """
        Initializes the graph with given node names.
        Creates an adjacency matrix with all values set to zero.
        """
        self.nodes = np.copy(sNames)
        self.n = len(self.nodes)
        self.adjacency = np.zeros((self.n, self.n))

    def addCopyOfEdge(self, edge):
        """
        Adds an undirected edge to the adjacency matrix using an Edge object.
        Updates both directions (i.e., bidirectional edge).
        """
        self.adjacency[edge.id1, edge.id2] = edge.weight
        self.adjacency[edge.id2, edge.id1] = edge.weight

    def addEdge(self, name1, name2, weight):
        """
        Adds an undirected edge between two nodes identified by their names.
        The edge weight is assigned symmetrically.
        """
        id1 = np.where(self.nodes == name1)[0][0]
        id2 = np.where(self.nodes == name2)[0][0]
        self.adjacency[id1, id2] = weight
        self.adjacency[id2, id1] = weight

    def addArc(self, name1, name2, weight):
        """
        Adds a directed edge (arc) from name1 to name2 with the given weight.
        """
        id1 = np.where(self.nodes == name1)[0][0]
        id2 = np.where(self.nodes == name2)[0][0]
        self.adjacency[id1, id2] = weight

    def addArcByIndex(self, id1, id2, weight):  
        """
        Adds a directed edge (arc) between nodes identified by their indices.
        """
        self.adjacency[id1, id2] = weight

    def getArcs(self):
        """
        Returns a list of all directed edges (arcs) in the graph.
        """
        arcs = []
        for i in range(self.n):
            for j in range(self.n):
                if self.adjacency[i][j] != 0:
                    arcs.append(Edge(i, j, self.adjacency[i][j]))
        return arcs

    def getEdges(self):
        """
        Returns a list of all undirected edges in the graph.
        Only considers one direction to avoid duplicates.
        """
        edges = []
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.adjacency[i][j] != 0:
                    edges.append(Edge(i, j, self.adjacency[i][j]))
        return edges
        
    def createACycle(self, edge):
        """
        Checks whether adding a given edge creates a cycle in the graph.

        Uses a breadth-first traversal to explore connected components
        and detects cycles by checking if a visited node is encountered again.
        """
        cycleDetected = False
        reachedNodes = []
        reachedNodes.append(edge.id1)

        if edge.id2 in reachedNodes:
            cycleDetected = True
        else:
            reachedNodes.append(edge.id2)

        nodesToTest = []
        nodesToTest.append(edge.id1)
        nodesToTest.append(edge.id2)

        reachedEdges = []
        reachedEdges.append(Edge(edge.id1, edge.id2, edge.weight))

        while not cycleDetected and len(nodesToTest) > 0:

            currentNode = nodesToTest[0]
            nodesToTest.pop(0)

            neighborIndex = 0

            while not cycleDetected and neighborIndex < self.n:

                currentEdge = Edge(currentNode, neighborIndex, 1)

                # If there is an edge and it has not been visited before
                if self.adjacency[currentNode][neighborIndex] != 0.0 and not currentEdge in reachedEdges:

                    # If the node was already visited, a cycle is detected
                    if neighborIndex in reachedNodes:
                        cycleDetected = True 

                    # Otherwise, add this node to the list of visited nodes and nodes to test
                    else:
                        reachedNodes.append(neighborIndex)
                        reachedEdges.append(currentEdge)
                        nodesToTest.append(neighborIndex)
                    
                neighborIndex += 1

        return cycleDetected

    def indexOf(self, sName):
        """
        Retrieves the index of a node in the graph based on its name.
        sName: Name of the node
        return: Index of the node, or -1 if not found.
        """
        for i in range(len(self.nodes)):
            if self.nodes[i] == sName:
                return i
        
        return -1

    def __repr__(self):
        """
        Returns a string representation of the graph by listing all its edges.
        """

        result = ""
    
        for i in range(self.n):
            for j in range(self.n):
                if self.adjacency[i][j] != 0:
                
                    # If there is an undirected edge
                    if self.adjacency[i][j] == self.adjacency[j][i]:
                        
                        # If it's the first time we encounter this edge
                        if i < j:
                            result += repr(self.nodes[i]) + " - " + repr(self.nodes[j]) + " (" + repr(self.adjacency[i][j]) + ")\n" 
    
                    # If there is a directed edge
                    else:
                        result += repr(self.nodes[i]) + " -> " + repr(self.nodes[j]) + " (" + repr(self.adjacency[i][j]) + ")\n" 
    
        return result
