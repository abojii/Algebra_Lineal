# TODO for Program Modifications

## 1. Modify Models/entrada.py
- [ ] Update solicitar_coeficientes_nxn() to accept input in the form "m x n" (e.g., 3x3, 5x3).
- [ ] Parse this input to get number of equations (m) and number of variables (n).
- [ ] Request coefficients accordingly for an m x n system.

## 2. Modify Models/metodos.py
- [ ] Add a function to compute the rank of a matrix from its echelon form.
- [ ] This function will be used to determine the rank of the coefficient matrix and augmented matrix.

## 3. Modify Models/sistema.py
- [ ] Update resolver_sistema() to parse the matrix size input as "m x n".
- [ ] Use the updated entrada.solicitar_coeficientes_nxn() to get the augmented matrix.
- [ ] Use metodos.escalonada_matriz() to get echelon form.
- [ ] Compute ranks of coefficient and augmented matrices.
- [ ] Determine if the system has unique solution, infinite solutions, or no solution based on ranks.
- [ ] Display the solution type message accordingly.
- [ ] Adjust method calls to support rectangular matrices where possible, or limit to square matrices for substitution/elimination.
- [ ] Print the solution or appropriate message.
