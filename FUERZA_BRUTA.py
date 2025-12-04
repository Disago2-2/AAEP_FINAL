import itertools
import random

def generar_instancia_aleatoria(n_ciudades, max_distancia=100, seed=None):
    """
    Genera una matriz de distancias simétrica aleatoria para n_ciudades.
    La diagonal es 0 (distancia de una ciudad a sí misma).
    """
    if seed is not None:
        random.seed(seed)
    
    dist = [[0] * n_ciudades for _ in range(n_ciudades)]
    for i in range(n_ciudades):
        for j in range(i + 1, n_ciudades):
            d = random.randint(10, max_distancia)
            dist[i][j] = d
            dist[j][i] = d
    return dist


def costo_ruta(ruta, distancias):
    """Calcula la distancia total de una ruta cerrada (incluye regreso al inicio)."""
    total = 0
    for i in range(len(ruta) - 1):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[i + 1]
        total += distancias[ciudad_actual][ciudad_siguiente]
    return total


def tsp_fuerza_bruta(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    Resuelve el TSP por fuerza bruta:
    - Genera todas las permutaciones posibles de las ciudades (excepto la inicial).
    - Calcula el costo total de cada ruta que:
        ciudad_inicio -> ... -> ciudad_inicio
    - Devuelve la mejor ruta y su costo.
    """
    n = len(distancias)
    
    # Todas las ciudades excepto la ciudad de inicio
    otras_ciudades = [i for i in range(n) if i != ciudad_inicio]
    
    mejor_ruta = None
    mejor_costo = float('inf')
    
    num_permutaciones = 0
    
    # Generar todas las permutaciones posibles de las otras ciudades
    for perm in itertools.permutations(otras_ciudades):
        num_permutaciones += 1
        
        # Ruta completa: inicio -> permutación -> inicio
        ruta = [ciudad_inicio] + list(perm) + [ciudad_inicio]
        
        costo = costo_ruta(ruta, distancias)
        
        if costo < mejor_costo:
            mejor_costo = costo
            mejor_ruta = ruta
    
    # Si tenemos nombres de ciudades, convertimos índices a nombres
    if nombres_ciudades is not None:
        mejor_ruta_nombres = [nombres_ciudades[i] for i in mejor_ruta]
    else:
        mejor_ruta_nombres = mejor_ruta
    
    return mejor_ruta, mejor_ruta_nombres, mejor_costo, num_permutaciones


if __name__ == "__main__":
    # Ejemplo concreto de una empresa de envíos en Perú
    nombres_ciudades = [
        "Lima",      # 0
        "Arequipa",  # 1
        "Cusco",     # 2
        "Trujillo",  # 3
        "Piura"      # 4
    ]
    
    # Matriz de distancias ficticia (km) entre las ciudades:
    #        Li   Ar   Cu   Tr   Pi
    distancias = [
        [   0, 1000, 1100,  560,  980],  # Lima
        [1000,    0,  510, 1600, 1850],  # Arequipa
        [1100,  510,    0, 1300, 1500],  # Cusco
        [ 560, 1600, 1300,    0,  410],  # Trujillo
        [ 980, 1850, 1500,  410,    0]   # Piura
    ]
    
    # También podrías generar una instancia aleatoria:
    # distancias = generar_instancia_aleatoria(n_ciudades=5, max_distancia=200, seed=42)
    
    ciudad_inicio = 0  # Lima como punto de origen
    
    mejor_ruta_idx, mejor_ruta_nombres, mejor_costo, num_perm = tsp_fuerza_bruta(
        distancias,
        nombres_ciudades,
        ciudad_inicio
    )
    
    print("=== TSP por Fuerza Bruta ===")
    print(f"Ciudades: {nombres_ciudades}")
    print(f"Número de permutaciones evaluadas: {num_perm}")
    print("Mejor ruta (índices):", mejor_ruta_idx)
    print("Mejor ruta (nombres):", " -> ".join(mejor_ruta_nombres))
    print(f"Costo total de la mejor ruta: {mejor_costo} km")
