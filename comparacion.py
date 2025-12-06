import itertools
import time

# ==========================




# DATOS DEL PROBLEMA (EMPRESA DE ENVÍOS)
# ==========================

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


# ==========================
# FUNCIÓN AUXILIAR
# ==========================

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


# ==========================
# MÉTODO 1: FUERZA BRUTA (PERMUTACIONES)
# ==========================

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


# ==========================
# MÉTODO 2: RECURSIVO SIN MEMOIZACIÓN (BACKTRACKING)
# ==========================

def tsp_recursivo_sin_memo(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    TSP usando búsqueda recursiva (backtracking) SIN memoización.
    Explora todas las posibles rutas y se queda con la mejor.
    """
    n = len(distancias)

    # Arreglo booleano para saber qué ciudades ya se visitaron
    visitadas = [False] * n
    visitadas[ciudad_inicio] = True

    mejor_ruta = None
    mejor_costo = float('inf')

    # Ruta actual durante la recursión
    ruta_actual = [ciudad_inicio]

    # Contador de llamadas recursivas (para análisis)
    llamadas_recursivas = 0

    def backtrack(ciudad_actual, costo_actual):
        nonlocal mejor_ruta, mejor_costo, llamadas_recursivas
        llamadas_recursivas += 1

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

    return mejor_ruta, mejor_ruta_nombres, mejor_costo, llamadas_recursivas


# ==========================
# MÉTODO 3: RECURSIVO CON MEMOIZACIÓN (DP TOP-DOWN)
# ==========================

def tsp_top_down_memo(distancias, nombres_ciudades=None, ciudad_inicio=0):
    """
    TSP usando Programación Dinámica Top-Down (recursión + memoización).
    Estado: (ciudad_actual, visited_mask)
    visited_mask es un entero donde cada bit indica si una ciudad ya fue visitada.
    """
    n = len(distancias)
    ALL_VISITED = (1 << n) - 1  # ejemplo: n=4 -> 1111 (binario)

    # memo[(ciudad_actual, visited_mask)] = mejor costo para completar el viaje
    memo = {}
    # decision[(ciudad_actual, visited_mask)] = mejor siguiente ciudad
    decision = {}

    # Contador de llamadas a dp (para análisis)
    llamadas_dp = 0

    def dp(ciudad_actual, visited_mask):
        nonlocal llamadas_dp
        llamadas_dp += 1

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

    # Tamaño de la tabla memo (número de estados distintos)
    num_estados_memo = len(memo)

    return ruta_indices, ruta_nombres, mejor_costo, llamadas_dp, num_estados_memo


# ==========================
# PROGRAMA PRINCIPAL: COMPARAR LOS 3 MÉTODOS
# ==========================

if __name__ == "__main__":
    print("===== COMPARACIÓN DE MÉTODOS PARA TSP (EMPRESA DE ENVÍOS) =====\n")
    print("Ciudades:", nombres_ciudades)
    print()

    # ---------- Método 1: Fuerza Bruta ----------
    inicio = time.time()
    ruta1_idx, ruta1_nombres, costo1, rutas_eval_1 = tsp_fuerza_bruta(
        distancias, nombres_ciudades, ciudad_inicio
    )
    fin = time.time()
    tiempo1 = fin - inicio

    print("=== Método 1: Fuerza Bruta (permutaciones) ===")
    print("Mejor ruta:", " -> ".join(ruta1_nombres))
    print("Costo total:", costo1, "km")
    print("Número de rutas evaluadas:", rutas_eval_1)
    print(f"Tiempo aproximado de ejecución: {tiempo1:.6f} segundos\n")

    # ---------- Método 2: Recursivo sin memo ----------
    inicio = time.time()
    ruta2_idx, ruta2_nombres, costo2, llamadas2 = tsp_recursivo_sin_memo(
        distancias, nombres_ciudades, ciudad_inicio
    )
    fin = time.time()
    tiempo2 = fin - inicio

    print("=== Método 2: Recursivo SIN memoización (backtracking) ===")
    print("Mejor ruta:", " -> ".join(ruta2_nombres))
    print("Costo total:", costo2, "km")
    print("Número de llamadas recursivas:", llamadas2)
    print(f"Tiempo aproximado de ejecución: {tiempo2:.6f} segundos\n")

    # ---------- Método 3: Recursivo con memo ----------
    inicio = time.time()
    ruta3_idx, ruta3_nombres, costo3, llamadas3, estados_memo = tsp_top_down_memo(
        distancias, nombres_ciudades, ciudad_inicio
    )
    fin = time.time()
    tiempo3 = fin - inicio

    print("=== Método 3: Recursivo CON memoización (DP Top-Down) ===")
    print("Mejor ruta:", " -> ".join(ruta3_nombres))
    print("Costo total:", costo3, "km")
    print("Número de llamadas a dp:", llamadas3)
    print("Número de estados distintos en memo:", estados_memo)
    print(f"Tiempo aproximado de ejecución: {tiempo3:.6f} segundos\n")

    # ---------- Resumen comparativo ----------
    print("===== RESUMEN COMPARATIVO =====")
    print(f"{'Método':40s} {'Costo':>10s} {'Tiempo (s)':>12s} {'Medida de esfuerzo':>22s}")
    print("-" * 90)
    print(f"{'Fuerza Bruta (permutaciones)':40s} {str(costo1):>10s} {tiempo1:12.6f} {('Rutas: ' + str(rutas_eval_1)):>22s}")
    print(f"{'Recursivo sin memo (backtracking)':40s} {str(costo2):>10s} {tiempo2:12.6f} {('Llamadas: ' + str(llamadas2)):>22s}")
    print(f"{'Recursivo con memo (DP Top-Down)':40s} {str(costo3):>10s} {tiempo3:12.6f} {('Estados memo: ' + str(estados_memo)):>22s}")
