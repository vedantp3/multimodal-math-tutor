# Linear Algebra Formulas & Identities

## Matrix Operations
- (A + B)ᵀ = Aᵀ + Bᵀ
- (AB)ᵀ = BᵀAᵀ
- (kA)ᵀ = kAᵀ
- (A⁻¹)ᵀ = (Aᵀ)⁻¹

## Determinants
### 2×2 Matrix
det([a b; c d]) = ad - bc

### 3×3 Matrix (Sarrus' Rule / Cofactor Expansion)
det(A) = a(ei - fh) - b(di - fg) + c(dh - eg)
for A = [a b c; d e f; g h i]

### Properties
- det(AB) = det(A) · det(B)
- det(Aᵀ) = det(A)
- det(kA) = kⁿ · det(A) for n×n matrix
- det(A⁻¹) = 1/det(A)
- If any row/column is all zeros, det = 0
- Swapping two rows changes sign of det

## Matrix Inverse
### 2×2 Matrix
A⁻¹ = (1/det(A)) · [d -b; -c a]

### Using Adjoint
A⁻¹ = adj(A) / det(A)
A matrix is invertible iff det(A) ≠ 0

## Systems of Linear Equations (Cramer's Rule)
For Ax = b:
x_i = det(A_i) / det(A)
where A_i has column i replaced by b

## Eigenvalues and Eigenvectors
- Characteristic equation: det(A - λI) = 0
- Eigenvalue equation: Av = λv
- Sum of eigenvalues = trace(A)
- Product of eigenvalues = det(A)

## Rank of a Matrix
- rank(A) = number of non-zero rows in row echelon form
- rank(A) ≤ min(m, n) for m×n matrix
- System Ax = b is consistent iff rank(A) = rank([A|b])

## Vector Operations
- Dot product: a · b = |a||b|cos(θ)
- Cross product: |a × b| = |a||b|sin(θ)
- Projection of a on b: proj_b(a) = (a · b / |b|²) · b
