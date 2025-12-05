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


















def tsp_recursivo_sin_memo(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    TSP usando búsqueda recursiva (backtracking) SIN memoización.
    Explora todas las posibles rutas recursivamente y se queda con la mejor.
    """
    n = len(distancias)

    # Arreglo booleano para saber qué ciudades ya se visitaron
    visitadas = [False] * n
    visitadas[ciudad_inicio] = True

    mejor_ruta = None
    mejor_costo = float('inf')

    # Ruta actual durante la recursión
    ruta_actual = [ciudad_inicio]

    def backtrack(ciudad_actual, costo_actual):
        nonlocal mejor_ruta, mejor_costo

        # Si ya visitamos todas las ciudades, regresamos al inicio
        if len(ruta_actual) == n:
            costo_total = costo_actual + distancias[ciudad_actual][ciudad_inicio]
            if costo_total < mejor_costo:
                mejor_costo = costo_total
                # Ruta completa incluyendo el regreso al inicio
                mejor_ruta = ruta_actual[:] + [ciudad_inicio]
            return

        # Probar ir a cualquier ciudad no visitada
        for siguiente in range(n):
            if not visitadas[siguiente]:
                visitadas[siguiente] = True
                ruta_actual.append(siguiente)

                nuevo_costo = costo_actual + distancias[ciudad_actual][siguiente]
                backtrack(siguiente, nuevo_costo)

                # deshacemos la decisión (backtracking)
                ruta_actual.pop()
                visitadas[siguiente] = False

    # Llamada inicial
    backtrack(ciudad_inicio, 0)

    # Convertimos índices a nombres si corresponde
    if nombres_ciudades is not None:
        mejor_ruta_nombres = [nombres_ciudades[i] for i in mejor_ruta]
    else:
        mejor_ruta_nombres = mejor_ruta

    return mejor_ruta, mejor_ruta_nombres, mejor_costo


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

    mejor_ruta_idx, mejor_ruta_nombres, mejor_costo = tsp_recursivo_sin_memo(
        distancias,
        nombres_ciudades,
        ciudad_inicio
    )

    print("=== TSP Recursivo SIN memoización (backtracking) ===")
    print("Mejor ruta (índices):", mejor_ruta_idx)
    print("Mejor ruta (nombres):", " -> ".join(mejor_ruta_nombres))
    print("Costo total:", mejor_costo, "km")
