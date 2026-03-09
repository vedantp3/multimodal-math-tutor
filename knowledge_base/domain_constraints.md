# Domain Constraints & Validity Rules

## General Rules
- **Division by zero**: Any expression with a denominator must have denominator ≠ 0
- **Square root domain**: √x requires x ≥ 0 for real-valued results
- **Logarithm domain**: log(x) requires x > 0
- **Even root domain**: ⁿ√x for even n requires x ≥ 0
- **Trigonometric domains**: tan(x) undefined at x = π/2 + nπ; sec(x), csc(x) have similar restrictions

## Algebraic Constraints
- Quadratic discriminant: b² - 4ac ≥ 0 for real roots
- Absolute value: |x| ≥ 0 always
- For polynomial equations of degree n, expect at most n roots (counting multiplicity)
- AM-GM inequality requires non-negative terms

## Calculus Constraints
- Differentiability requires continuity (but not vice versa)
- Integration bounds must avoid discontinuities of the integrand
- Maxima/minima on a closed interval must include boundary checks
- Taylor series convergence: always check the radius of convergence

## Probability Constraints
- 0 ≤ P(A) ≤ 1 for any event A
- Σ P(all outcomes) = 1
- Probabilities cannot be negative
- Number of permutations/combinations must be non-negative integers
- C(n,r) is defined only for 0 ≤ r ≤ n where n, r are non-negative integers

## Linear Algebra Constraints
- Matrix multiplication A·B requires: columns of A = rows of B
- Inverse exists only if det(A) ≠ 0
- Eigenvalues of a real symmetric matrix are always real
- Rank ≤ min(rows, columns)

## JEE-Specific Validity
- Check all answer choices if it's an MCQ — verify by elimination
- In "find the range" problems, always verify endpoints
- For inequality proofs, check boundary conditions
- In optimization problems, verify the critical point is indeed a max/min, not just a saddle point
