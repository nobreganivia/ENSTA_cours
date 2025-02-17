from mpi4py import MPI
import numpy as np

def bucket_sort(arr):
    #Trie un tableau en utilisant le Bucket Sort.
    if len(arr) == 0:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    bucket_count = len(arr) // 2 or 1  # Nombre de buckets
    buckets = [[] for _ in range(bucket_count)]
    
    for num in arr:
        index = int((num - min_val) / (max_val - min_val + 1) * (bucket_count - 1))
        buckets[index].append(num)
    
    for i in range(bucket_count):
        buckets[i].sort()
    
    return [num for bucket in buckets for num in bucket]

# Initialisation de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 100  # Taille du tableau à trier
if rank == 0:
    # Processus maître génère les nombres aléatoires
    data = np.random.randint(0, 1000, N)
    print(f"Processus {rank}: Données générées {data}\n")
    
    # Détermination des intervalles pour chaque bucket
    min_val, max_val = min(data), max(data)
    range_size = (max_val - min_val + 1) // size + 1
    
    # Création des buckets
    buckets = [[] for _ in range(size)]
    for num in data:
        index = (num - min_val) // range_size
        buckets[index].append(num)
else:
    buckets = None

# Distribution des buckets aux processus
local_data = comm.scatter(buckets, root=0)
copy_local_data = [int(num) for num in local_data]  
print(f"Processus {rank}: Reçu {copy_local_data}\n")

# Chaque processus trie son bucket
sorted_local_data = bucket_sort(local_data)
copy_sorted_local_data = [int(num) for num in sorted_local_data]

print(f"Processus {rank}: Bucket trié {copy_sorted_local_data}\n")

# Collecte des données triées sur le processus 0
sorted_data = comm.gather(sorted_local_data, root=0)

if rank == 0:
    # Fusionner tous les buckets triés
    sorted_data = [int(num) for bucket in sorted_data for num in bucket]

    print(f"Processus {rank}: Tableau final trié {sorted_data}")
