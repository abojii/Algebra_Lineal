import math

def safe_eval(expr, x_val):
    """Evalúa de forma segura una función matemática como string."""
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed_names['x'] = x_val
    try:
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        raise ValueError(f"Error en la función: {e}")

def calcular_error_relativo(xr, xr_prev):
    """Calcula el error relativo porcentual."""
    if xr_prev is None or xr == 0:
        return float('inf')
    return abs((xr - xr_prev) / xr) * 100

def metodo_regla_falsa(f_expr: str, a: float, b: float, tol: float, max_iter: int = 100):
    """
    Ejecuta el método de Regla Falsa (False Position).

    Parámetros:
        f_expr (str): Función f(x) como cadena (Ej: "x**3 - x - 1")
        a (float): Límite inferior
        b (float): Límite superior
        tol (float): Tolerancia del error
        max_iter (int): Máximo de iteraciones

    Retorna:
        xr (float): Raíz aproximada
        iteraciones (int): Total de iteraciones realizadas
        error (float): Error relativo final
        historial (list): Lista de diccionarios con los valores por iteración
    """
    fa = safe_eval(f_expr, a)
    fb = safe_eval(f_expr, b)

    if fa * fb >= 0:
        raise ValueError("El intervalo no es válido. f(a) y f(b) deben tener signos opuestos.")

    xr_prev = None
    error_rel = float('inf')
    iteraciones = []
    iter_count = 0

    while error_rel > tol and iter_count < max_iter:
        iter_count += 1

        # Punto de intersección
        xr = b - (fb * (b - a)) / (fb - fa)
        fxr = safe_eval(f_expr, xr)

        error_rel = calcular_error_relativo(xr, xr_prev)
        xr_prev = xr

        # Guardar datos de la iteración
        iteraciones.append({
            "iter": iter_count,
            "a": a,
            "b": b,
            "xr": xr,
            "f_xr": fxr,
            "error": error_rel,
            "intervalo": [a, b]
        })

        # Actualización del intervalo
        if fa * fxr < 0:
            b = xr
            fb = fxr
        else:
            a = xr
            fa = fxr

    return xr, iter_count, error_rel, iteraciones
