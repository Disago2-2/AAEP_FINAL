import itertools

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


def calcular_costo_ruta(ruta, distancias):
    """
    Suma las distancias de la ruta cerrada:
    ciudad[0] -> ciudad[1] -> ... -> ciudad[n-1] -> ciudad[0]
    """
    total = 0
    for i in range(len(ruta) - 1):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[i + 1]
        total += distancias[ciudad_actual][ciudad_siguiente]
    return total


def tsp_fuerza_bruta(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    Resuelve el TSP por fuerza bruta generando todas las rutas posibles
    que comienzan y terminan en ciudad_inicio.
    """
    n = len(distancias)

    # Lista de todas las ciudades excepto la de inicio
    otras_ciudades = []
    for i in range(n):
        if i != ciudad_inicio:
            otras_ciudades.append(i)

    mejor_ruta = None
    mejor_costo = float('inf')
    num_rutas_evaluadas = 0

    # Recorremos todas las permutaciones posibles de las otras ciudades
    for perm in itertools.permutations(otras_ciudades):
        # Construimos la ruta completa incluyendo el regreso al inicio
        ruta = [ciudad_inicio] + list(perm) + [ciudad_inicio]

        costo = calcular_costo_ruta(ruta, distancias)
        num_rutas_evaluadas += 1

        if costo < mejor_costo:
            mejor_costo = costo
            mejor_ruta = ruta

    # Convertimos índices a nombres si los tenemos
    if nombres_ciudades is not None:
        mejor_ruta_nombres = []
        for idx in mejor_ruta:
            mejor_ruta_nombres.append(nombres_ciudades[idx])
    else:
        mejor_ruta_nombres = mejor_ruta

    return mejor_ruta, mejor_ruta_nombres, mejor_costo, num_rutas_evaluadas


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

    ciudad_inicio = 0  # Lima

    mejor_ruta_idx, mejor_ruta_nombres, mejor_costo, num_rutas = tsp_fuerza_bruta(
        distancias,
        nombres_ciudades,
        ciudad_inicio
    )

    print("=== TSP por Fuerza Bruta (permutaciones) ===")
    print("Ciudades:", nombres_ciudades)
    print("Número de rutas evaluadas:", num_rutas)
    print("Mejor ruta (índices):", mejor_ruta_idx)
    print("Mejor ruta (nombres):", " -> ".join(mejor_ruta_nombres))
    print("Costo total:", mejor_costo, "km")
