import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
import time
import matplotlib.cm
from mpi4py import MPI
import matplotlib.pyplot as plt

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex, smooth=False) -> float:
        z = 0
        for i in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return i + 1 - log(log(abs(z))) / log(2)
                return i
        return self.max_iterations

# Initialisation MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Paramètres de l'ensemble de Mandelbrot
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3.0 / width
scaleY = 2.25 / height

# Répartition améliorée : plus de charge pour le centre
lines_per_process = np.array([height // size] * size, dtype=int)

# Donner plus de lignes aux processus qui calculent la zone centrale
if size > 1:
    extra_lines = height % size
    for i in range(extra_lines):
        lines_per_process[i] += 1  # Répartir les lignes restantes

# Calculer les indices de début et de fin pour chaque processus
start_line = sum(lines_per_process[:rank])
end_line = start_line + lines_per_process[rank]

# Initialisation du tableau local
local_convergence = np.empty((end_line - start_line, width), dtype=np.double)

# Calcul de l'ensemble de Mandelbrot
deb = time.time()
for y in range(start_line, end_line):
    for x in range(width):
        c = complex(-2.0 + scaleX * x, -1.125 + scaleY * y)
        local_convergence[y - start_line, x] = mandelbrot_set.convergence(c, smooth=True)
fin = time.time()
print(f"Process {rank}: Temps du calcul de l'ensemble de Mandelbrot : {fin - deb:.4f} s")

# Collecte des résultats dans le processus 0
recv_counts = np.array([lines_per_process[i] * width for i in range(size)], dtype=int)
recv_displs = np.array([sum(recv_counts[:i]) for i in range(size)], dtype=int)
convergence = np.empty((height, width), dtype=np.double) if rank == 0 else None

comm.Gatherv(sendbuf=local_convergence.ravel(), recvbuf=(convergence, recv_counts, recv_displs, MPI.DOUBLE) if rank == 0 else None, root=0)

# Génération de l'image et sauvegarde (uniquement sur rank 0)
if rank == 0:
    deb_image = time.time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence) * 255))
    image.save("mandel.png")
    fin_image = time.time()
    print(f"Temps de constitution de l'image : {fin_image - deb_image:.4f} secondes")

# Calcul du speedup (collecte des temps)
execution_time = np.array(fin - deb)
all_times = np.zeros(size) if rank == 0 else None
comm.Gather(execution_time, all_times, root=0)

if rank == 0:
    speedup = all_times[0] / all_times
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, size+1), speedup, marker='o', linestyle='-', label="Speedup Mesuré")
    plt.plot(range(1, size+1), range(1, size+1), linestyle="--", color="gray", label="Speedup Idéal (Linéaire)")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Nombre de processus")
    plt.ylabel("Speedup")
    plt.title("Speedup avec MPI (répartition optimisée)")
    plt.legend()
    plt.grid(True)
    plt.show()
