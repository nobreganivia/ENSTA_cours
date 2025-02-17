import numpy as np
import graph
import sys

def main():
    # Créer un graphe contenant les sommets a, b, c, d, e, f, g 
    g = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g"]))

    # Ajouter les arêtes
    g.addEdge("a", "b",  1.0)
    g.addEdge("a", "c",  3.0)
    g.addEdge("b", "c",  2.0)
    g.addEdge("b", "d",  5.0)
    g.addEdge("b", "e",  7.0)
    g.addEdge("b", "f",  9.0)
    g.addEdge("c", "d",  4.0)
    g.addEdge("d", "e",  6.0)
    g.addEdge("d", "g", 12.0)
    g.addEdge("e", "f",  8.0)
    g.addEdge("e", "g", 11.0)
    g.addEdge("f", "g", 10.0)
    
    # Créer d'autres graphes pour les exercices 3.5
    h = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g", "h"]))
    h.addEdge("a", "b", 9.0)
    h.addEdge("a", "f", 6.0)
    h.addEdge("a", "h", 9.0)
    h.addEdge("b", "e", 5.0)
    h.addEdge("b", "c", 5.0)
    h.addEdge("b", "d", 8.0)
    h.addEdge("c", "g", 5.0)
    h.addEdge("c", "d", 2.0)
    h.addEdge("d", "g", 8.0)
    h.addEdge("d", "h", 7.0)
    h.addEdge("e", "f", 1.0)
    h.addEdge("e", "g", 3.0)
    h.addEdge("g", "h", 5.0)
    
    k = graph.Graph(np.array(["A", "B", "C", "D", "E", "F"]))
    k.addEdge("A", "B", 4.0)
    k.addEdge("A", "C", 3.0)
    k.addEdge("B", "C", 5.0)
    k.addEdge("B", "F", 2.0)
    k.addEdge("C", "F", 5.0)
    k.addEdge("C", "D", 2.0)
    k.addEdge("D", "F", 3.0)
    k.addEdge("D", "E", 4.0)
    k.addEdge("E", "F", 3.0)
    
    # Obtenir un arbre couvrant de poids minimal du graphe
    tree_g = kruskal(g)
    tree_h = kruskal(h)
    tree_k = kruskal(k)
    
    # Afficher les résultats
    print("Exercice 1:")
    print(tree_g if tree_g else "Pas d'arbre couvrant pour g")
    
    print("Exercice 3, gauche:")
    print(tree_h if tree_h else "Pas d'arbre couvrant pour h")
    
    print("Exercice 3, droite:")
    print(tree_k if tree_k else "Pas d'arbre couvrant pour k")

def kruskal(g):
    # Crée un nouvel arbre vide avec les mêmes nœuds que le graphe d'origine
    tree = graph.Graph(g.nodes)
    
    # Récupère toutes les arêtes du graphe
    edges = g.getEdges()
    
    # Trie les arêtes par poids croissant
    edges.sort()
    
    # Initialise un dictionnaire pour stocker les parents de chaque nœud (utilisé pour l'union-find)
    parent = {node: node for node in g.nodes}

    # Fonction pour trouver la racine d'un nœud (avec compression de chemin)
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])  # Compression de chemin
        return parent[node]

    # Fonction pour unir deux ensembles
    def union(node1, node2):
        root1 = find(node1)  # Trouve la racine du premier nœud
        root2 = find(node2)  # Trouve la racine du deuxième nœud
        if root1 != root2:
            parent[root2] = root1  # Union des deux ensembles
            return True
        return False

    # Parcourt toutes les arêtes triées par poids
    for edge in edges:
        # Récupère les noms des nœuds à partir de leurs indices
        node1 = g.nodes[edge.id1]
        node2 = g.nodes[edge.id2]
        
        # Si les deux nœuds ne sont pas dans le même ensemble, ajoute l'arête à l'arbre
        if union(node1, node2):
            tree.addEdge(node1, node2, edge.weight)

    # Vérifie si l'arbre a le bon nombre d'arêtes (n-1 pour un graphe connexe)
    return tree if len(tree.getEdges()) == len(g.nodes) - 1 else None

if __name__ == '__main__':
    main()
