import graph
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
    # Obtenir l'index de l'origine
    r = g.indexOf(origin)
    
    # Prochain nœud considéré
    pivot = r
    
    # Liste qui contiendra les sommets ayant été considérés comme pivot
    v2 = [r]
    
    pred = [-1] * g.n
    
    # Les distances entre r et les autres sommets sont initialement infinies
    pi = [sys.float_info.max] * g.n
    pi[r] = 0
    
    for _ in range(g.n - 1):
        for y in range(g.n):
            if y not in v2 and g.adjacency[pivot][y] > 0:
                new_distance = pi[pivot] + g.adjacency[pivot][y]
                if new_distance < pi[y]:
                    pi[y] = new_distance
                    pred[y] = pivot
        
        pivot = -1
        min_distance = sys.float_info.max
        for z in range(g.n):
            if z not in v2 and pi[z] < min_distance:
                min_distance = pi[z]
                pivot = z
        
        if pivot == -1:
            break
        
        v2.append(pivot)
    
    return pi, pred

if __name__ == '__main__':
    main()
