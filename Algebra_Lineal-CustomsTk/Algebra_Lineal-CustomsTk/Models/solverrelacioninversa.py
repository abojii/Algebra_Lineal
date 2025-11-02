class InverseRelationSolver:
    def __init__(self, determinant_solver):
        self.det_solver = determinant_solver

    def check_invertibility(self, matrix):
        det = self.det_solver.det_cofactor(matrix)
        return det != 0, det

    def interpret_invertibility(self, det):
        return self.det_solver.interpret_invertibility(det)
