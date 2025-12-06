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

def tsp_top_down_memo(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    TSP usando Programación Dinámica Top-Down (recursión + memoización explícita).
    Estado: (ciudad_actual, visited_mask)
    visited_mask es un entero donde cada bit indica si una ciudad ya fue visitada.
    """
    n = len(distancias)
    ALL_VISITED = (1 << n) - 1  # ejemplo: n=4 -> 1111 (binario)

    # memo[(ciudad_actual, visited_mask)] = mejor costo para completar el viaje
    memo = {}
    # decision[(ciudad_actual, visited_mask)] = mejor siguiente ciudad desde ese estado
    decision = {}

    def dp(ciudad_actual, visited_mask):
        """
        Devuelve el costo mínimo para:
        - Estar en ciudad_actual,
        - Habiendo visitado el conjunto de ciudades indicado por visited_mask,
        - Y completar el recorrido visitando todas y regresando al inicio.
        """
        clave = (ciudad_actual, visited_mask)

        # Si ya lo calculamos antes, lo devolvemos
        if clave in memo:
            return memo[clave]

        # Caso base: todas las ciudades visitadas
        if visited_mask == ALL_VISITED:
            costo_regreso = distancias[ciudad_actual][ciudad_inicio]
            memo[clave] = costo_regreso
            decision[clave] = ciudad_inicio
            return costo_regreso

        mejor_costo = float('inf')
        mejor_siguiente = None

        # Probar ir a cualquier ciudad no visitada
        for siguiente in range(n):
            # Si el bit de 'siguiente' está apagado, no se ha visitado
            if (visited_mask & (1 << siguiente)) == 0:
                nuevo_mask = visited_mask | (1 << siguiente)
                costo_ir = distancias[ciudad_actual][siguiente]
                costo_restante = dp(siguiente, nuevo_mask)
                costo_total = costo_ir + costo_restante

                if costo_total < mejor_costo:
                    mejor_costo = costo_total
                    mejor_siguiente = siguiente

        memo[clave] = mejor_costo
        decision[clave] = mejor_siguiente
        return mejor_costo

    # Llamada inicial: solo la ciudad de inicio está visitada
    visited_mask_inicial = (1 << ciudad_inicio)
    mejor_costo = dp(ciudad_inicio, visited_mask_inicial)

    # Reconstrucción de la ruta óptima usando 'decision'
    ruta_indices = [ciudad_inicio]
    ciudad_actual = ciudad_inicio
    visited_mask = visited_mask_inicial

    while visited_mask != ALL_VISITED:
        clave = (ciudad_actual, visited_mask)
        siguiente = decision[clave]
        ruta_indices.append(siguiente)
        visited_mask = visited_mask | (1 << siguiente)
        ciudad_actual = siguiente

    # Volvemos al origen
    ruta_indices.append(ciudad_inicio)

    # Convertimos a nombres
    if nombres_ciudades is not None:
        ruta_nombres = [nombres_ciudades[i] for i in ruta_indices]
    else:
        ruta_nombres = ruta_indices

    return ruta_indices, ruta_nombres, mejor_costo


if __name__ == "__main__":
    nombres_ciudades = [
        "Lima",
        "Arequipa",
        "Cusco",
        "Trujillo",
        "Piura"
    ]

    distancias = [
        [   0, 1000, 1100,  560,  980],
        [1000,    0,  510, 1600, 1850],
        [1100,  510,    0, 1300, 1500],
        [ 560, 1600, 1300,    0,  410],
        [ 980, 1850, 1500,  410,    0]
    ]

    ciudad_inicio = 0

    ruta_idx, ruta_nombres, mejor_costo = tsp_top_down_memo(
        distancias,
        nombres_ciudades,
        ciudad_inicio
    )

    print("=== TSP DP Top-Down CON memoización ===")
    print("Mejor ruta (índices):", ruta_idx)
    print("Mejor ruta (nombres):", " -> ".join(ruta_nombres))
    print("Costo total:", mejor_costo, "km")
