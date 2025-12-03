import math

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

def metodo_secante(f_expr, x0, x1, tol, max_iter=100):
    xr_old = None
    Ea = float("inf")
    iteracion = 0
    historial = []
    paso_a_paso = []

    while Ea > tol and iteracion < max_iter:
        iteracion += 1

        f0 = safe_eval(f_expr, x0)
        f1 = safe_eval(f_expr, x1)

        if f1 - f0 == 0:
            raise ValueError("f(x1) - f(x0) = 0. Método diverge.")

        xr = x1 - f1 * (x1 - x0) / (f1 - f0)
        Ea = error_rel(xr, xr_old)
        prev_xr = xr_old
        xr_old = xr

        # Detalle en texto
        detalle = f"Iteración {iteracion} (Secante)\n"
        detalle += f"x0 = {f6(x0)}, x1 = {f6(x1)}\n"
        detalle += f"f(x0) = f({f6(x0)}) = {f6(f0)}\n"
        detalle += f"f(x1) = f({f6(x1)}) = {f6(f1)}\n"
        detalle += f"x_r = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0)) = {f6(x1)} - ({f6(f1)})*({f6(x1)} - {f6(x0)})/({f6(f1)} - {f6(f0)}) = {f6(xr)}\n"
        if prev_xr is None:
            detalle += "E_a = N/A (primera iteración)\n"
        else:
            detalle += f"E_a = |({f6(xr)} - {f6(prev_xr)}) / {f6(xr)}| * 100 = {f6(Ea)} %\n"
        detalle += "--------------------------------------------------\n\n"
        paso_a_paso.append(detalle)

        historial.append({
            "iter": iteracion,
            "xl": f6(x0),
            "xu": f6(x1),
            "xr": f6(xr),
            "Ea": f6(0 if Ea == float("inf") else Ea),
            "vl": f6(f0),
            "vu": f6(f1),
            "vr": "-",  # No aplica
        })

        x0 = x1
        x1 = xr

    paso_a_paso_str = "".join(paso_a_paso)
    return f6(xr), iteracion, f6(Ea), historial, paso_a_paso_str