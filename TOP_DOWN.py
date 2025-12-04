from functools import lru_cache

def tsp_top_down(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    TSP usando programación dinámica Top-Down (memoización).
    - distancias: matriz de tamaño n x n
    - ciudad_inicio: índice de la ciudad de origen
    Devuelve: (mejor_ruta_indices, mejor_ruta_nombres, mejor_costo)
    """
    n = len(distancias)
    ALL_VISITED = (1 << n) - 1  # máscara con todos los bits en 1

    @lru_cache(maxsize=None)
    def dp(ciudad_actual, visited_mask):
        """
        dp(ciudad_actual, visited_mask) = costo mínimo para:
        - Estar en ciudad_actual
        - Habiendo visitado el conjunto de ciudades 'visited_mask'
        - Y completar el recorrido visitando todas y regresando al inicio
        """
        # Si ya visitamos todas, regresar al inicio
        if visited_mask == ALL_VISITED:
            return distancias[ciudad_actual][ciudad_inicio]

        mejor = float('inf')
        for siguiente in range(n):
            if not (visited_mask & (1 << siguiente)):
                nuevo_mask = visited_mask | (1 << siguiente)
                costo = distancias[ciudad_actual][siguiente] + dp(siguiente, nuevo_mask)
                if costo < mejor:
                    mejor = costo
        return mejor

    # Costo óptimo comenzando desde ciudad_inicio habiendo visitado solo esa
    mejor_costo = dp(ciudad_inicio, 1 << ciudad_inicio)

    # Reconstrucción de la ruta óptima
    ruta_indices = [ciudad_inicio]
    visited_mask = 1 << ciudad_inicio
    ciudad_actual = ciudad_inicio

    while visited_mask != ALL_VISITED:
        mejor_siguiente = None
        mejor_val = float('inf')

        for siguiente in range(n):
            if not (visited_mask & (1 << siguiente)):
                nuevo_mask = visited_mask | (1 << siguiente)
                # usamos la misma función dp para decidir el mejor siguiente
                val = distancias[ciudad_actual][siguiente] + dp(siguiente, nuevo_mask)
                if val < mejor_val:
                    mejor_val = val
                    mejor_siguiente = siguiente

        ruta_indices.append(mejor_siguiente)
        visited_mask |= (1 << mejor_siguiente)
        ciudad_actual = mejor_siguiente

    # Volvemos al inicio
    ruta_indices.append(ciudad_inicio)

    if nombres_ciudades is not None:
        ruta_nombres = [nombres_ciudades[i] for i in ruta_indices]
    else:
        ruta_nombres = ruta_indices

    return ruta_indices, ruta_nombres, mejor_costo


if __name__ == "__main__":
    # Mismas ciudades del ejemplo de fuerza bruta
    nombres_ciudades = [
        "Lima",      # 0
        "Arequipa",  # 1
        "Cusco",     # 2
        "Trujillo",  # 3
        "Piura"      # 4
    ]

    distancias = [
        [   0, 1000, 1100,  560,  980],  # Lima
        [1000,    0,  510, 1600, 1850],  # Arequipa
        [1100,  510,    0, 1300, 1500],  # Cusco
        [ 560, 1600, 1300,    0,  410],  # Trujillo
        [ 980, 1850, 1500,  410,    0]   # Piura
    ]

    ciudad_inicio = 0  # Lima

    ruta_idx, ruta_nombres, mejor_costo = tsp_top_down(
        distancias,
        nombres_ciudades,
        ciudad_inicio
    )

    print("=== TSP DP Top-Down (Memoización) ===")
    print("Mejor ruta (índices):", ruta_idx)
    print("Mejor ruta (nombres):", " -> ".join(ruta_nombres))
    print(f"Costo total de la mejor ruta: {mejor_costo} km")
