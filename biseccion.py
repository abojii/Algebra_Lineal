import math

def safe_eval(expr, x_val):
    """Evalúa de forma segura una función matemática dada como string."""
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


def metodo_biseccion(f_expr: str, a: float, b: float, tol: float, max_iter: int = 100):
    """
    Ejecuta el método de bisección.

    Parámetros:
        f_expr: str      → la función f(x) como string, ej: "math.exp(x)-3*x"
        a: float         → límite inferior
        b: float         → límite superior
        tol: float       → tolerancia del error
        max_iter: int    → máximo de iteraciones

    Retorna:
        raiz_aproximada: float
        iteraciones_totales: int
        error_final: float
        historial: list de dicts con valores por iteración
    """
    fa = safe_eval(f_expr, a)
    fb = safe_eval(f_expr, b)

    if fa * fb >= 0:
        raise ValueError("El intervalo no es válido. f(a) y f(b) deben tener signos opuestos.")

    iteraciones = []
    xr_prev = None
    error_rel = float('inf')
    iter_count = 0

    while error_rel > tol and iter_count < max_iter:
        iter_count += 1
        xr = (a + b) / 2
        fxr = safe_eval(f_expr, xr)

        # Error relativo
        error_rel = calcular_error_relativo(xr, xr_prev)
        xr_prev = xr

        # Guardar la iteración
        iteraciones.append({
            "iter": iter_count,
            "a": a,
            "b": b,
            "xr": xr,
            "f_xr": fxr,
            "error": error_rel,
            "intervalo": [a, b]
        })

        # Actualizar el intervalo
        if fa * fxr < 0:
            b = xr
        else:
            a = xr
            fa = fxr  # actualiza fa si a cambia

    return xr, iter_count, error_rel, iteraciones
