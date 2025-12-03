import math
import sympy as sp  # Agregar import de SymPy

def safe_eval(expr, x_val):
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    allowed["x"] = x_val
    return float(eval(expr, {"__builtins__": {}}, allowed))

def error_rel(xr, xrold):
    if xrold is None:
        return float("inf")
    return abs((xr - xrold) / xr) * 100

def f6(n):
    return float(f"{n:.6f}")

def metodo_newton_raphson(f_expr, x0, tol, max_iter=100):
    # Convertir f_expr a expresión simbólica
    x = sp.Symbol('x')
    try:
        f_sym = sp.sympify(f_expr)  # Convertir string a simbólico
        df_sym = sp.diff(f_sym, x)  # Calcular derivada simbólica
    except Exception as e:
        raise ValueError(f"Error al procesar la función: {e}")

    xr_old = None
    Ea = float("inf")
    iteracion = 0
    historial = []
    paso_a_paso = []

    while Ea > tol and iteracion < max_iter:
        iteracion += 1

        fx = safe_eval(f_expr, x0)  # Evaluar f(x0) numéricamente
        dfx = float(df_sym.subs(x, x0))  # Evaluar f'(x0) numéricamente

        if dfx == 0:
            raise ValueError("Derivada cero en x0. Método diverge.")

        xr = x0 - fx / dfx
        Ea = error_rel(xr, xr_old)
        prev_xr = xr_old
        xr_old = xr

        # Detalle en texto
        detalle = f"Iteración {iteracion} (Newton-Raphson)\n"
        detalle += f"x0 = {f6(x0)}\n"
        detalle += f"f(x0) = f({f6(x0)}) = {f6(fx)}\n"
        detalle += f"f'(x0) = f'({f6(x0)}) = {f6(dfx)}\n"
        detalle += f"x_r = x0 - f(x0)/f'(x0) = {f6(x0)} - ({f6(fx)})/({f6(dfx)}) = {f6(xr)}\n"
        if prev_xr is None:
            detalle += "E_a = N/A (primera iteración)\n"
        else:
            detalle += f"E_a = |({f6(xr)} - {f6(prev_xr)}) / {f6(xr)}| * 100 = {f6(Ea)} %\n"
        detalle += "--------------------------------------------------\n\n"
        paso_a_paso.append(detalle)

        historial.append({
            "iter": iteracion,
            "xl": f6(x0),  # Usamos xl para x0
            "xu": "-",     # No aplica
            "xr": f6(xr),
            "Ea": f6(0 if Ea == float("inf") else Ea),
            "vl": f6(fx),  # vl para f(x0)
            "vu": f6(dfx), # vu para f'(x0)
            "vr": "-",     # No aplica
        })

        x0 = xr

    paso_a_paso_str = "".join(paso_a_paso)
    return f6(xr), iteracion, f6(Ea), historial, paso_a_paso_str