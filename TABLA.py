def tsp_bottom_up(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    TSP usando programación dinámica Bottom-Up (Held–Karp).
    - distancias: matriz n x n
    - ciudad_inicio: índice de la ciudad de origen
    Devuelve: (mejor_ruta_indices, mejor_ruta_nombres, mejor_costo)
    """
    n = len(distancias)
    N_MASK = 1 << n
    INF = float('inf')

    # dp[mask][j] = costo mínimo para ir desde ciudad_inicio
    # visitando el subconjunto 'mask' (que incluye j) y terminando en j
    dp = [[INF] * n for _ in range(N_MASK)]
    parent = [[-1] * n for _ in range(N_MASK)]

    # Caso base: solo la ciudad de inicio está visitada y estamos en ella
    dp[1 << ciudad_inicio][ciudad_inicio] = 0

    for mask in range(N_MASK):
        # Si la ciudad de inicio no está en el subconjunto, ignoramos
        if not (mask & (1 << ciudad_inicio)):
            continue

        for j in range(n):
            if not (mask & (1 << j)):
                continue  # j no está en el subconjunto

            if j == ciudad_inicio and mask != (1 << ciudad_inicio):
                # No queremos volver al inicio en medio del recorrido
                continue

            # mask sin la ciudad j (subconjunto previo)
            prev_mask = mask ^ (1 << j)
            if prev_mask == 0 and j != ciudad_inicio:
                continue  # subconjunto inválido

            if prev_mask == 0 and j == ciudad_inicio:
                # caso base ya inicializado
                continue

            # Probamos todos los posibles k que venían antes de j
            for k in range(n):
                if not (prev_mask & (1 << k)):
                    continue

                nuevo_costo = dp[prev_mask][k] + distancias[k][j]
                if nuevo_costo < dp[mask][j]:
                    dp[mask][j] = nuevo_costo
                    parent[mask][j] = k

    # Reconstruimos la solución óptima:
    ALL_VISITED = (1 << n) - 1
    mejor_costo = INF
    mejor_ultima = -1

    # Terminamos en alguna ciudad j (≠ inicio) y regresamos al inicio
    for j in range(n):
        if j == ciudad_inicio:
            continue
        costo_total = dp[ALL_VISITED][j] + distancias[j][ciudad_inicio]
        if costo_total < mejor_costo:
            mejor_costo = costo_total
            mejor_ultima = j

    # Reconstruir el camino óptimo desde parent[][]
    ruta_indices = []
    mask = ALL_VISITED
    ciudad_actual = mejor_ultima

    # Ruta en orden inverso desde ciudad_actual hasta ciudad_inicio
    while ciudad_actual != -1:
        ruta_indices.append(ciudad_actual)
        prev = parent[mask][ciudad_actual]
        mask ^= (1 << ciudad_actual)
        ciudad_actual = prev

    # Ahora ruta_indices tiene algo como [última, ..., inicio]
    ruta_indices.reverse()

    # Aseguramos que inicie en ciudad_inicio
    if ruta_indices[0] != ciudad_inicio:
        # Si por alguna razón no inicia, lo forzamos
        if ciudad_inicio in ruta_indices:
            idx = ruta_indices.index(ciudad_inicio)
            ruta_indices = ruta_indices[idx:] + ruta_indices[1:idx]
        else:
            ruta_indices.insert(0, ciudad_inicio)

    # Volvemos al origen para cerrar el ciclo
    ruta_indices.append(ciudad_inicio)

    if nombres_ciudades is not None:
        ruta_nombres = [nombres_ciudades[i] for i in ruta_indices]
    else:
        ruta_nombres = ruta_indices

    return ruta_indices, ruta_nombres, mejor_costo


if __name__ == "__main__":
    # Mismas ciudades e instancia que antes (puedes cambiarla si quieres)
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

    ruta_idx, ruta_nombres, mejor_costo = tsp_bottom_up(
        distancias,
        nombres_ciudades,
        ciudad_inicio
    )

    print("=== TSP DP Bottom-Up (Held–Karp) ===")
    print("Mejor ruta (índices):", ruta_idx)
    print("Mejor ruta (nombres):", " -> ".join(ruta_nombres))
    print(f"Costo total de la mejor ruta: {mejor_costo} km")
