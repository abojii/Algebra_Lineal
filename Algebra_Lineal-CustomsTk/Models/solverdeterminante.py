class DeterminantSolver:
    def __init__(self):
        self.steps = []
        
    def get_minor(self, M, i, j):
        n = len(M)
        if n == 0 or any(len(row) != n for row in M):
            raise ValueError("La matriz debe ser cuadrada y no vacía.")
        return [[row[c] for c in range(n) if c != j]
                for r, row in enumerate(M) if r != i]

    def det_cofactor(self, M, _top=True):
        # Normaliza a listas y a números por si llegan strings/tuplas
        M = [list(row) for row in M]
        n = len(M)
        if n == 0 or any(len(row) != n for row in M):
            raise ValueError("La matriz debe ser cuadrada y no vacía.")
        for r in range(n):
            for c in range(n):
                v = M[r][c]
                if isinstance(v, str):
                    M[r][c] = float(v) if '.' in v else int(v)

        if _top:
            self.steps = []  # limpiamos solo en el nivel superior

        # Casos base
        if n == 1:
            return M[0][0]
        if n == 2:
            return M[0][0]*M[1][1] - M[0][1]*M[1][0]

        # Elige la fila con más ceros (menos costo)
        def nonzeros(row): return sum(1 for x in row if x != 0)
        i = min(range(n), key=lambda r: nonzeros(M[r]))

        det = 0
        for j, aij in enumerate(M[i]):
            if aij == 0:
                if _top:
                    self.steps.append(f"a[{i},{j}]=0 ⇒ término 0")
                continue
            minor = self.get_minor(M, i, j)
            subdet = self.det_cofactor(minor, _top=False)
            sign = -1 if ((i + j) % 2) else 1  # (-1)^(i+j)
            term = sign * aij * subdet
            det += term

            if _top:
                self.steps.append(
                    f"a[{i},{j}]={aij}, signo={sign}, det(menor[{i},{j}])={subdet}, "
                    f"término={term}"
                )
        return det
    def det_cramer(self, matrix):
        # (Laplace por primera fila; útil para matrices pequeñas)
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            det = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
            self.steps = [f"Det(A) = ({matrix[0][0]}×{matrix[1][1]}) - ({matrix[0][1]}×{matrix[1][0]}) = {det}"]
            return det
        det = 0
        steps = []
        for j in range(n):
            minor = self.get_minor(matrix, 0, j)
            cofactor = ((-1) ** (0 + j)) * self.det_cramer(minor)
            det += matrix[0][j] * cofactor
            steps.append(f"C[0,{j}]={cofactor}, término={matrix[0][j]}·{cofactor}={matrix[0][j]*cofactor}")
        self.steps = steps
        return det

    def det_sarrus(self, M):
        if len(M) != 3 or len(M[0]) != 3:
            raise ValueError("Sarrus solo aplica a 3x3.")
        a,b,c = M[0], M[1], M[2]
        dp = a[0]*b[1]*c[2] + a[1]*b[2]*c[0] + a[2]*b[0]*c[1]
        ds = a[2]*b[1]*c[0] + a[1]*b[0]*c[2] + a[0]*b[2]*c[1]
        det = dp - ds
        self.steps = [f"Diag+={dp}", f"Diag-={ds}", f"Det={dp}-{ds}={det}"]
        return det

    # --- helpers opcionales (chequeos, multiplicación) se quedan igual ---
    # ... (tus check_property1..5 y multiply_matrices como los tienes)

    @staticmethod
    def debug_top_terms(A):
        """Muestra los 3 términos de la expansión por la primera fila (3x3)."""
        obj = DeterminantSolver()
        terms = []
        for j, a0j in enumerate(A[0]):
            minor = obj.get_minor(A, 0, j)
            subdet = obj.det_cofactor(minor)
            sign = 1 if (j % 2 == 0) else -1
            term = sign * a0j * subdet
            terms.append((j, minor, subdet, term))
        total = sum(t[3] for t in terms)
        return terms, total

