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

def metodo_regla_falsa(f_expr, a, b, tol, max_iter=100):
    fa = safe_eval(f_expr, a)
    fb = safe_eval(f_expr, b)

    if fa * fb >= 0:
        raise ValueError("El intervalo no es válido. f(a) y f(b) deben tener signos opuestos.")

    xr_old = None
    Ea = float("inf")
    iteracion = 0
    historial = []
    paso_a_paso = []

    while Ea > tol and iteracion < max_iter:
        iteracion += 1

        xl = a
        xu = b
        vl = fa
        vu = fb

        # Regla falsa: xr = xu - f(xu)*(xl - xu)/(f(xl) - f(xu))
        xr = xu - (vu * (xl - xu)) / (vl - vu)
        vr = safe_eval(f_expr, xr)

        Ea = error_rel(xr, xr_old)
        prev_xr = xr_old
        xr_old = xr

        # ---------- detalle en texto ----------
        detalle = f"Iteración {iteracion} (Regla Falsa)\n"
        detalle += f"x_l = {f6(xl)}, x_u = {f6(xu)}\n"
        detalle += f"v_l = f(x_l) = f({f6(xl)}) = {f6(vl)}\n"
        detalle += f"v_u = f(x_u) = f({f6(xu)}) = {f6(vu)}\n"
        detalle += (
            f"x_r = x_u - v_u * (x_l - x_u) / (v_l - v_u)\n"
            f"    = {f6(xu)} - ({f6(vu)} * ({f6(xl)} - {f6(xu)})) / "
            f"({f6(vl)} - {f6(vu)}) = {f6(xr)}\n"
        )
        detalle += f"v_r = f(x_r) = f({f6(xr)}) = {f6(vr)}\n"
        if prev_xr is None:
            detalle += "E_a = N/A (primera iteración)\n"
        else:
            detalle += (
                f"E_a = |({f6(xr)} - {f6(prev_xr)}) / {f6(xr)}| * 100 = {f6(Ea)} %\n"
            )
        if vl * vr < 0:
            detalle += "Como v_l * v_r < 0, el nuevo intervalo es [x_l, x_r].\n"
        else:
            detalle += "Como v_l * v_r >= 0, el nuevo intervalo es [x_r, x_u].\n"
        detalle += "--------------------------------------------------\n\n"
        paso_a_paso.append(detalle)
        # --------------------------------------

        # actualizar intervalo
        if vl * vr < 0:
            b = xr
            fb = vr
        else:
            a = xr
            fa = vr

        historial.append({
            "iter": iteracion,
            "xl": f6(xl),
            "xu": f6(xu),
            "xr": f6(xr),
            "Ea": f6(0 if Ea == float("inf") else Ea),
            "vl": f6(vl),
            "vu": f6(vu),
            "vr": f6(vr),
        })

    paso_a_paso_str = "".join(paso_a_paso)
    return f6(xr), iteracion, f6(Ea), historial, paso_a_paso_str
