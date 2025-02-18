# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`

## lscpu

*lscpu donne des infos utiles sur le processeur : nb core, taille de cache :*

```
Coller ici les infos *utiles* de lscpu.

Architecture:             x86_64
  CPU op-mode(s):         32-bit, 64-bit
  Address sizes:          39 bits physical, 48 bits virtual
  Byte Order:             Little Endian
CPU(s):                   4
  On-line CPU(s) list:    0-3
Vendor ID:                GenuineIntel
  Model name:             Intel(R) Core(TM) i5-7200U CPU @ 2.50GHz
    CPU family:           6
    Model:                142
    Thread(s) per core:   2
    Core(s) per socket:   2
    Socket(s):            1
    Stepping:             9
    BogoMIPS:             5424.00
    Flags:                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtsc
                          p lm constant_tsc arch_perfmon rep_good nopl xtopology cpuid pni pclmulqdq ssse3 fma cx16 pdcm pcid sse4_1 sse4_2 movbe popcnt a
                          es xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti ssbd ibrs ibpb stibp fsgsbase bmi1 avx2 smep bm
                          i2 erms invpcid rdseed adx smap clflushopt xsaveopt xsavec xgetbv1 xsaves md_clear flush_l1d arch_capabilities
Virtualization features:  
  Hypervisor vendor:      Microsoft
  Virtualization type:    full
Caches (sum of all):      
  L1d:                    64 KiB (2 instances)
  L1i:                    64 KiB (2 instances)
  L2:                     512 KiB (2 instances)
  L3:                     3 MiB (1 instance)
```


## Produit matrice-matrice

### Effet de la taille de la matrice

  n            | MFlops
---------------|--------
1024 (origine) | 83.7643
1023           | 104.979
2000           | 105.142
2048           | 73.5372
2049           | 103.664

*Expliquer les résultats.*

Les résultats montrent que les performances de la multiplication de matrices dépendent fortement de la taille de la matrice et de son alignement mémoire. Les tailles qui ne sont pas des puissances de 2 (comme 1023, 2000 et 1060) peuvent éviter les conflits de cache et exploiter mieux la localité des données, ce qui se traduit par de meilleures performances en MFlops. En revanche, les tailles qui sont des puissances de 2 (comme 1024 et 2048) peuvent souffrir de conflits de cache et de défauts d'alignement, ce qui réduit les performances.

### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`

make TestProduct.exe
Compile uniquement l'exécutable TestProduct.exe en suivant les règles du Makefile;
Utilise les options de compilation définies (comme -O3, -march=native).

./TestProduct.exe 1024
Exécute le programme avec une taille de matrice de 1024x1024;
Le nombre 1024 est passé comme argument pour définir la taille des matrices;
Ce choix permet de tester les performances avec une taille courante (puissance de 2).




  ordre           | time    | MFlops  | MFlops(n=2048)
------------------|---------|---------|----------------
i,j,k (origine)   | 2.73764 | 782.476 | 176.434
j,i,k             | 8.05702 | 266.536 | 178.479
i,k,j             | 26.3245 | 81.5774 | 76.7866
k,i,j             | 27.8361 | 77.1474 | 73.8179
j,k,i             | 0.93883 | 2287.39 | 2037.51
k,j,i             | 1.07396 | 1999.6  | 1996.24


*Discuter les résultats.*

Impact de l'ordre des boucles:
L'ordre des boucles (i,j,k, j,i,k, etc.) affecte la manière dont les données sont accédées en mémoire;
Un bon ordre de boucles maximise la localité des données, c'est-à-dire l'utilisation efficace du cache du processeur.

i,j,k et j,i,k:
Ces ordres ont des performances moyennes car ils ne maximisent pas la localité des données.
L'accès à la mémoire est moins efficace, ce qui entraîne plus de défauts de cache (cache misses).

i,k,j et k,i,j:
Ces ordres ont les pires performances;
Ils provoquent un grand nombre de défauts de cache car les données sont accédées de manière non séquentielle.

j,k,i et k,j,i:
Ces ordres ont les meilleures performances;
Ils maximisent la localité des données en accédant à la mémoire de manière séquentielle, réduisant ainsi les défauts de cache.


### OMP sur la meilleure boucle

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1                 | 2352.76 |   2305.12      |    2315.55     |   2143.51
2                 | 1861.91 |   2186.32      |    2066.32     |   2159.22
3                 | 2221.09 |   2296.12      |    2572.2      |   2170.49
4                 | 2358.84 |   2281.12      |    1083.85     |   1886.72
5                 | 2294.46 |   2248.69      |    2438.2      |   2138.08
6                 | 2370.38 |   2310.77      |    2583.21     |   2143.06
7                 | 2194.4  |   2278.68      |    2518.96     |   2128.13
8                 | 2300.42 |   2263.45      |    2232.04     |   2067.9

*Tracer les courbes de speedup (pour chaque valeur de n), discuter les résultats.*

n=512
Observations :
Le speedup n'est pas linéaire et varie de manière irrégulière.
Pour N=4, le speedup chute significativement (0.47), ce qui suggère une mauvaise répartition de la charge ou des conflits de cache.
Pour N=6, le speedup atteint son maximum (1.12), ce qui indique une bonne parallélisation.
Explications :
Pour les petites matrices (n=512), la surcharge liée à la gestion des threads (création, synchronisation) peut dominer les gains de performance.

n=1024
Observations :
Le speedup est proche de 1 pour la plupart des valeurs de N, sauf pour 
N=2 (0.79).
Cela suggère que la parallélisation n'apporte pas de gains significatifs pour cette taille de matrice.
Explications :
La taille de la matrice (n=1024) est peut-être trop petite pour tirer pleinement parti de la parallélisation.

n=2048
Observations :
Le speedup est relativement stable, variant entre 0.95 et 1.01.
Cela indique que la parallélisation est efficace, mais les gains sont limités.
Explications :
Pour cette taille de matrice, la parallélisation fonctionne bien, mais les défauts de cache et la surcharge de gestion des threads limitent les gains.

n=4096
Observations :
Le speedup est stable, variant entre 0.96 et 1.01.
Cela montre que la parallélisation est efficace, mais les gains sont modestes.
Explications :
Pour les grandes matrices (n=4096), la parallélisation est efficace, mais la taille des données peut entraîner des défauts de cache et une saturation de la bande passante mémoire.

### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
32                | 2217.9  |   2178.08      |  2429.16       |   2137.35
64                | 2179.31 |   2277.91      |  2451.61       |   2116.64
128               | 1768.8  |   1835.47      |  2205.04       |   2154.78
256               | 2342.35 |   2307.75      |  2431.47       |   2083.98
512               | 2350.63 |   2271.23      |  2554.02       |   2134.37
1024              | 2336.22 |   2261.61      |  2581.33       |   1985.28

*Discuter les résultats.*

Taille du bloc (szBlock) :
La taille du bloc affecte la manière dont les données sont accédées en mémoire et stockées dans le cache;
Une taille de bloc trop petite (szBlock = 32) peut entraîner une surcharge due à la gestion des blocs;
Une taille de bloc trop grande (szBlock = 1024) peut dépasser la capacité du cache, entraînant des défauts de cache (cache misses);
Une taille de bloc intermédiaire (szBlock = 64, 256, 512) permet généralement un bon équilibre entre la localité des données et la gestion des blocs.

Localité des données :
Une taille de bloc optimale permet de maximiser la localité des données, c'est-à-dire l'utilisation efficace du cache;
Pour szBlock = 128, la localité des données est moins efficace, ce qui explique la chute des performances.


### Bloc + OMP


  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|----------------|----------------|---------------|
1024           |  1      |2288.78  | 2340.29        |   2533.77      | 2062.26       |
1024           |  8      | 2268.27 |   2325.69      |    1916.25     |    2101.77    |
512            |  1      | 2305.55 |    2342.3      |    2520.22     |  2129.44      |
512            |  8      |  2398.33|   2379.56      |    1829.08     |   2139.15     |

*Discuter les résultats.*

Taille du bloc (szBlock) :
Une taille de bloc plus grande (szBlock = 1024) permet de mieux exploiter la localité des données pour les grandes matrices, mais peut entraîner des défauts de cache pour les petites matrices;
Une taille de bloc plus petite (szBlock = 512) peut être plus efficace pour les petites matrices, mais peut limiter les performances pour les grandes matrices en raison de la surcharge liée à la gestion des blocs.

Nombre de threads (OMP_NUM) :
Avec OMP_NUM = 1, le programme fonctionne en mode séquentiel, ce qui permet d'éviter la surcharge liée à la gestion des threads;
Avec OMP_NUM = 8, le programme utilise plusieurs threads pour paralléliser la multiplication de matrices. Cela peut améliorer les performances pour les grandes matrices, mais entraîne une surcharge pour les petites matrices.

Les résultats montrent que le choix de la taille du bloc (szBlock) et du nombre de threads (OMP_NUM) a un impact significatif sur les performances de la multiplication de matrices. Pour maximiser les performances, il est important de choisir une taille de bloc et un nombre de threads adaptés à la taille de la matrice. En général :
Utilisez une taille de bloc plus grande (szBlock = 1024) pour les grandes matrices (n = 2048, 4096);
Utilisez une taille de bloc plus petite (szBlock = 512) pour les petites matrices (n = 512);
Utilisez un nombre de threads plus élevé (OMP_NUM = 8) pour les grandes matrices, mais préférez un seul thread (OMP_NUM = 1) pour les petites matrices.

### Comparaison avec BLAS

*Comparer les performances avec un calcul similaire utilisant les bibliothèques d'algèbre linéaire BLAS, Eigen et/ou numpy.*

Dans deux petits tests:
./test_product_matrice_blas.exe 1024
Test passed
Temps CPU produit matrice-matrice blas : 0.0493253 secondes
MFlops -> 43537.1

 ./test_product_matrice_blas.exe 4096
Test passed
Temps CPU produit matrice-matrice blas : 2.35741 secondes
MFlops -> 58300.8

L'utilisation de la bibliothèque BLAS pour le produit matrice-matrice montre des performances extrêmement élevées, atteignant 43537.1 MFlops pour n = 1024 et 58300.8 MFlops pour n = 4096. Ces résultats soulignent l'efficacité des implémentations optimisées de BLAS, qui exploitent des techniques avancées d'optimisation matérielle.