import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, '.')

try:
    from solverdeterminante import DeterminantSolver
    from solverrelacioninversa import InverseRelationSolver
except ImportError:
    try:
        from Models.solverdeterminante import DeterminantSolver
        from Models.solverrelacioninversa import InverseRelationSolver
    except ImportError:
        sys.path.insert(0, '..')
        from Models.solverdeterminante import DeterminantSolver
        from Models.solverrelacioninversa import InverseRelationSolver

def test_determinant_methods():
    solver = DeterminantSolver()

    # Test matrices
    matrices = [
        [[1, 2], [3, 4]],  # 2x2, det = -2
        [[1, 2, 3], [4, 5, 6], [7, 8, 10]],  # 3x3, det = -3
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]],  # Identity, det = 1
        [[0, 0], [0, 0]],  # Zero matrix, det = 0
        [[1, 2], [2, 4]],  # Proportional rows, det = 0
        [[2, -1, 3], [0, 4, 5], [1, -2, 6]],  # User's matrix, det should be 51
    ]

    for i, A in enumerate(matrices):
        print(f"\n--- Matrix {i+1}: {A} ---")
        n = len(A)

        # Test Cramer if applicable
        if n <= 3:
            det_cramer = solver.det_cramer(A)
            print(f"Cramer det: {det_cramer}")
            print("Steps:", solver.steps)

        # Test Sarrus if 3x3
        if n == 3:
            det_sarrus = solver.det_sarrus(A)
            print(f"Sarrus det: {det_sarrus}")
            print("Steps:", solver.steps)

        # Test Cofactores
        det_cof = solver.det_cofactor(A)
        print(f"Cofactores det: {det_cof}")
        print("Steps:", solver.steps)

        # Invertibility
        print("Invertibility:", solver.interpret_invertibility(det_cof))

        # Properties
        print("Prop 1 (zero row/col):", solver.check_property1(A))
        print("Prop 2 (equal/prop rows/cols):", solver.check_property2(A))
        print("Prop 3 (swap sign):", solver.check_property3(A))
        print("Prop 4 (multiply row):", solver.check_property4(A))
        print("Prop 5 (det(AB)=detA*detB):", solver.check_property5(A))

def test_inverse_relation():
    det_solver = DeterminantSolver()
    inv_solver = InverseRelationSolver(det_solver)

    matrices = [
        [[1, 0], [0, 1]],  # Invertible
        [[1, 2], [3, 4]],  # Invertible
        [[0, 0], [0, 0]],  # Not invertible
    ]

    for i, A in enumerate(matrices):
        print(f"\n--- Inverse Test Matrix {i+1}: {A} ---")
        is_inv, det = inv_solver.check_invertibility(A)
        interpret = inv_solver.interpret_invertibility(det)
        print(f"Invertible: {is_inv}, Det: {det}")
        print(f"Interpretation: {interpret}")

if __name__ == "__main__":
    test_determinant_methods()
    test_inverse_relation()
