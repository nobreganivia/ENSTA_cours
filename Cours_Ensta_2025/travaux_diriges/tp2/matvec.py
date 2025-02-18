from mpi4py import MPI
import numpy as np
import time

# Initialisation MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()  # nbp (nombre total de tâches)

# Dimension de la matrice (modifiable, doit être divisible par size)
N = 120  

if N % size != 0:
    if rank == 0:
        print("Erreur : La dimension N doit être divisible par le nombre de processus MPI.")
    MPI.Finalize()
    exit()

# Calcul du nombre de lignes par processus
Nloc = N // size  

# Initialisation du vecteur u (identique pour tous)
if rank == 0:
    u = np.array([i + 1. for i in range(N)], dtype=np.float64)
else:
    u = np.empty(N, dtype=np.float64)  # Allocation vide pour u

# Broadcast du vecteur u à tous les processus
comm.Bcast(u, root=0)

# Chaque processus construit uniquement ses propres lignes de A
start_row = rank * Nloc
end_row = start_row + Nloc

A_local = np.array([[(i + j) % N + 1. for i in range(N)] for j in range(start_row, end_row)], dtype=np.float64)

# Synchronisation et début du chronomètre
comm.Barrier()
start_time = MPI.Wtime()

# Calcul du produit matrice-vecteur local
v_local = np.dot(A_local, u)

# Synchronisation avant la collecte des résultats
comm.Barrier()
end_time = MPI.Wtime()

# Assemblage du vecteur final `v` via Allgather (chaque processus reçoit `v` complet)
v = np.empty(N, dtype=np.float64)
comm.Allgather(v_local, v)

# Mesure du temps séquentiel pour le speed-up
if rank == 0:
    A = np.array([[(i + j) % N + 1. for i in range(N)] for j in range(N)], dtype=np.float64)
    start_seq = time.time()
    v_seq = np.dot(A, u)
    end_seq = time.time()
    T1 = end_seq - start_seq  # Temps séquentiel

    # Calcul du speed-up
    Tp = end_time - start_time
    speedup = T1 / Tp if Tp > 0 else 0
    print(f"Temps séquentiel : {T1:.6f} secondes")
    print(f"Temps parallèle avec {size} processus : {Tp:.6f} secondes")
    print(f"Speed-up obtenu avec {size} processus : {speedup:.2f}")

# Affichage du vecteur résultat (uniquement pour vérification)
if rank == 0:
    print(f"v = {v}")
