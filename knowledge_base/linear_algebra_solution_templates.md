# Linear Algebra Solution Templates

## Template: Solving Systems of Linear Equations
**Step 1**: Write the augmented matrix [A|b]
**Step 2**: Apply row operations to reach Row Echelon Form (REF)
**Step 3**: Check for consistency: if rank(A) = rank([A|b])
**Step 4**: Back-substitute to find the solution
**Step 5**: If free variables exist, express the solution in parametric form
**Check**: Substitute solution back into original equations

## Template: Finding Determinants
**Step 1**: For 2×2: ad - bc
**Step 2**: For 3×3: Use cofactor expansion along the row/column with the most zeros
**Step 3**: Expand using cofactors: det(A) = Σ (-1)^(i+j) · a_ij · M_ij
**Step 4**: Simplify recursively for sub-determinants
**Shortcut**: Use row operations to simplify before expanding (but track sign changes)

## Template: Finding Matrix Inverse
**Step 1**: Compute det(A). If det(A) = 0, the inverse does not exist
**Step 2**: For 2×2: A⁻¹ = (1/det(A)) · [d, -b; -c, a]
**Step 3**: For larger matrices: Form [A|I], apply row operations to get [I|A⁻¹]
**Step 4**: Verify: A · A⁻¹ = I
**Check**: (A⁻¹)⁻¹ = A

## Template: Eigenvalue Problems
**Step 1**: Set up characteristic equation: det(A - λI) = 0
**Step 2**: Expand and solve the polynomial for eigenvalues λ
**Step 3**: For each eigenvalue λ, solve (A - λI)v = 0 for eigenvector v
**Step 4**: Check: number of eigenvalues (counting multiplicity) equals the matrix size
**Step 5**: Verify: Av = λv for each eigenvalue-eigenvector pair

## Template: Cramer's Rule
**Step 1**: Compute D = det(A). If D = 0, Cramer's rule doesn't apply
**Step 2**: For each variable x_i, form matrix A_i by replacing column i of A with b
**Step 3**: Compute D_i = det(A_i)
**Step 4**: x_i = D_i / D
**Step 5**: Verify the solution
