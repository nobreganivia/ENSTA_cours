o objetivo com o codigo de Dijkstra é ir de Paris a Rana, corrija: import graph
import sys

def main():
    cities = ["Paris", "Hambourg", "Londres", "Amsterdam", "Edimbourg", "Berlin", "Stockholm", "Rana", "Oslo"]
    g = graph.Graph(cities)
    
    g.addArc("Paris", "Hambourg", 7)
    g.addArc("Paris", "Londres", 4)
    g.addArc("Paris", "Amsterdam", 3)
    g.addArc("Hambourg", "Stockholm", 1)
    g.addArc("Hambourg", "Berlin", 1)
    g.addArc("Londres", "Edimbourg", 2)
    g.addArc("Amsterdam", "Hambourg", 2)
    g.addArc("Amsterdam", "Oslo", 8)
    g.addArc("Stockholm", "Oslo", 2)
    g.addArc("Stockholm", "Rana", 5)
    g.addArc("Berlin", "Amsterdam", 2)
    g.addArc("Berlin", "Stockholm", 1)
    g.addArc("Berlin", "Oslo", 3)
    g.addArc("Edimbourg", "Oslo", 7)
    g.addArc("Edimbourg", "Amsterdam", 3)
    g.addArc("Edimbourg", "Rana", 6)
    g.addArc("Oslo", "Rana", 2)
    
    # Applique l'algorithme de Dijkstra pour obtenir une arborescence
    tree = dijkstra(g, "Paris")
    print(tree)

def dijkstra(g, origin):
    # Get the index of the origin 
    r = g.indexOf(origin)
    # Next node considered 
    pivot = r
    
    # Liste qui contiendra les sommets ayant été considérés comme pivot
    v2 = [r]
    pred = [-1] * g.n
    
    # Les distances entre r et les autres sommets sont initialement infinies
    pi = [sys.float_info.max] * g.n
    pi[r] = 0
    
    for _ in range(g.n - 1):
        for y in range(g.n):
            if y not in v2 and g.adjacency[pivot][y] != 0.0:
                if pi[pivot] + g.adjacency[pivot][y] < pi[y]:
                    pi[y] = pi[pivot] + g.adjacency[pivot][y]
                    pred[y] = pivot
        
        pivot = -1
        for z in range(g.n):
            if z not in v2 and (pivot == -1 or pi[z] < pi[pivot]):
                pivot = z
        
        v2.append(pivot)
    
    tree = graph.Graph(g.nodes)
    for x in range(g.n):
        if x != r and pred[x] != -1:
            tree.addArc(g.nodes[pred[x]], g.nodes[x], g.adjacency[pred[x]][x])
    
    print("Distances minimales depuis", g.nodes[r])
    for i in range(g.n):
        print(f"{g.nodes[r]} -> {g.nodes[i]}: {pi[i]}")
    
    return tree

if __name__ == '__main__':
    main()