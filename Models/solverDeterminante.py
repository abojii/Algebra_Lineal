class DeterminantSolver:
    def __init__(self):
        self.steps = []

    def det_cramer(self, matrix, indent=""):
        """
        Calcula el determinante usando un método recursivo similar a la expansión de cofactores,
        adecuado para matrices pequeñas (método de Cramer ilustrativo).
        Muestra pasos detallados y limpios paso a paso.
        """
        n = len(matrix)
        self.steps.append(f"{indent}Método de Cramer (expansión recursiva por cofactores) para matriz {n}x{n}:")
        self.steps.append(f"{indent}Matriz:")
        for row in matrix:
            self.steps.append(f"{indent}  {row}")

        if n == 1:
            det = matrix[0][0]
            self.steps.append(f"{indent}Det = {det}")
            return det
        elif n == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            self.steps.append(f"{indent}Det = ({matrix[0][0]} * {matrix[1][1]}) - ({matrix[0][1]} * {matrix[1][0]}) = {det}")
            return det

        det = 0
        self.steps.append(f"{indent}Expansión por fila 0:")
        for j in range(n):
            minor = self.get_minor(matrix, 0, j)
            self.steps.append(f"{indent}  Columna {j}: a[0][{j}] = {matrix[0][j]}, signo = (-1)^{{0 + {j}}} = {(-1)**(0+j)}")
            cofactor_val = self.det_cramer(minor, f"{indent}    ")
            cofactor = ((-1)**(0+j)) * cofactor_val
            product = matrix[0][j] * cofactor
            det += product
            self.steps.append(f"{indent}    C[0][{j}] = {cofactor}, producto = {matrix[0][j]} * {cofactor} = {product} (acumulado: {det})")
        self.steps.append(f"{indent}Det = {det}")
        return det

    def det_sarrus(self, matrix, indent=""):
        """
        Calcula el determinante usando la regla de Sarrus para matrices 3x3.
        Muestra pasos detallados y limpios paso a paso.
        """
        if len(matrix) != 3 or len(matrix[0]) != 3:
            raise ValueError("La regla de Sarrus solo aplica a matrices 3x3.")
        self.steps.append(f"{indent}Regla de Sarrus para matriz 3x3:")
        self.steps.append(f"{indent}Matriz:")
        for row in matrix:
            self.steps.append(f"{indent}  {row}")
        
        a, b, c = matrix[0], matrix[1], matrix[2]
        diag_principal = a[0] * b[1] * c[2] + a[1] * b[2] * c[0] + a[2] * b[0] * c[1]
        diag_secundaria = a[2] * b[1] * c[0] + a[1] * b[0] * c[2] + a[0] * b[2] * c[1]
        det = diag_principal - diag_secundaria
        
        self.steps.append(f"{indent}Diagonal principal: {a[0]}*{b[1]}*{c[2]} + {a[1]}*{b[2]}*{c[0]} + {a[2]}*{b[0]}*{c[1]} = {diag_principal}")
        self.steps.append(f"{indent}Diagonal secundaria: {a[2]}*{b[1]}*{c[0]} + {a[1]}*{b[0]}*{c[2]} + {a[0]}*{b[2]}*{c[1]} = {diag_secundaria}")
        self.steps.append(f"{indent}Det = {diag_principal} - {diag_secundaria} = {det}")
        return det

    def det_cofactor(self, matrix, indent=""):
        """
        Calcula el determinante usando expansión por cofactores para cualquier matriz cuadrada.
        Muestra pasos detallados y limpios paso a paso.
        """
        n = len(matrix)
        self.steps.append(f"{indent}Expansión por cofactores para matriz {n}x{n}:")
        self.steps.append(f"{indent}Matriz:")
        for row in matrix:
            self.steps.append(f"{indent}  {row}")

        if n == 1:
            det = matrix[0][0]
            self.steps.append(f"{indent}Det = {det}")
            return det
        elif n == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            self.steps.append(f"{indent}Det = ({matrix[0][0]} * {matrix[1][1]}) - ({matrix[0][1]} * {matrix[1][0]}) = {det}")
            return det

        det = 0
        self.steps.append(f"{indent}Expansión por fila 0:")
        for j in range(n):
            minor = self.get_minor(matrix, 0, j)
            self.steps.append(f"{indent}  Columna {j}: a[0][{j}] = {matrix[0][j]}, signo = (-1)^{{0 + {j}}} = {(-1)**(0+j)}")
            cofactor_val = self.det_cofactor(minor, f"{indent}    ")
            cofactor = ((-1)**(0+j)) * cofactor_val
            product = matrix[0][j] * cofactor
            det += product
            self.steps.append(f"{indent}    C[0][{j}] = {cofactor}, producto = {matrix[0][j]} * {cofactor} = {product} (acumulado: {det})")
        self.steps.append(f"{indent}Det = {det}")
        return det

    def get_minor(self, matrix, i, j):
        return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

    def check_property1(self, matrix):
        """
        Propiedad 1: Si una fila o columna es cero, entonces det(A) = 0.
        Retorna True si se cumple, False otherwise.
        """
        n = len(matrix)
        for i in range(n):
            if all(matrix[i][j] == 0 for j in range(n)):
                return True
            if all(matrix[j][i] == 0 for j in range(n)):
                return True
        return False

    def check_property2(self, matrix):
        """
        Propiedad 2: Si dos filas o columnas son iguales o proporcionales, entonces det(A) = 0.
        Retorna True si se cumple, False otherwise.
        """
        n = len(matrix)
        # Check rows
        for i in range(n):
            for k in range(i+1, n):
                if matrix[i] == matrix[k]:
                    return True
                # Check proportional
                ratio = None
                proportional = True
                for j in range(n):
                    if matrix[i][j] == 0 and matrix[k][j] == 0:
                        continue
                    if matrix[i][j] == 0 or matrix[k][j] == 0:
                        proportional = False
                        break
                    if ratio is None:
                        ratio = matrix[k][j] / matrix[i][j]
                    elif abs(matrix[k][j] / matrix[i][j] - ratio) > 1e-10:
                        proportional = False
                        break
                if proportional:
                    return True
        # Check columns
        for j in range(n):
            col1 = [matrix[i][j] for i in range(n)]
            for k in range(j+1, n):
                col2 = [matrix[i][k] for i in range(n)]
                if col1 == col2:
                    return True
                ratio = None
                proportional = True
                for i in range(n):
                    if col1[i] == 0 and col2[i] == 0:
                        continue
                    if col1[i] == 0 or col2[i] == 0:
                        proportional = False
                        break
                    if ratio is None:
                        ratio = col2[i] / col1[i]
                    elif abs(col2[i] / col1[i] - ratio) > 1e-10:
                        proportional = False
                        break
                if proportional:
                    return True
        return False

    def check_property3(self, matrix):
        """
        Propiedad 3: Si se intercambian dos filas, el determinante cambia de signo.
        Verifica con la primera y segunda fila.
        Retorna True si se cumple, False otherwise.
        """
        det1 = self.det_cofactor(matrix)
        if len(matrix) < 2:
            return True
        matrix_copy = [row[:] for row in matrix]
        matrix_copy[0], matrix_copy[1] = matrix_copy[1], matrix_copy[0]
        det2 = self.det_cofactor(matrix_copy)
        return abs(det2 + det1) < 1e-10

    def check_property4(self, matrix, k=2):
        """
        Propiedad 4: Si se multiplica una fila por un escalar k, el determinante se multiplica por k.
        Verifica con la primera fila.
        Retorna True si se cumple, False otherwise.
        """
        det1 = self.det_cofactor(matrix)
        matrix_copy = [row[:] for row in matrix]
        matrix_copy[0] = [x * k for x in matrix_copy[0]]
        det2 = self.det_cofactor(matrix_copy)
        return abs(det2 - det1 * k) < 1e-10

    def check_property5(self, matrix):
        """
        Propiedad 5: det(AB) = det(A) × det(B).
        Usa B como la matriz identidad para verificar.
        Retorna True si se cumple, False otherwise.
        """
        n = len(matrix)
        detA = self.det_cofactor(matrix)
        B = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        AB = self.multiply_matrices(matrix, B)
        detAB = self.det_cofactor(AB)
        detB = 1
        return abs(detAB - detA * detB) < 1e-10

    def multiply_matrices(self, A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def interpret_invertibility(self, det):
        if det != 0:
            return "El determinante es distinto de cero, por lo tanto A es invertible."
        else:
            return "El determinante es cero, la matriz no tiene inversa."
