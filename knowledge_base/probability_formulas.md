# Probability Formulas & Identities

## Basic Probability
- P(A) = Number of favorable outcomes / Total outcomes
- 0 ≤ P(A) ≤ 1
- P(A') = 1 - P(A) (complement)
- P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
- P(A ∪ B) = P(A) + P(B) if A and B are mutually exclusive

## Conditional Probability
- P(A|B) = P(A ∩ B) / P(B), where P(B) > 0
- P(A ∩ B) = P(A|B) · P(B) = P(B|A) · P(A)

## Bayes' Theorem
P(A|B) = P(B|A) · P(A) / P(B)
P(A_i|B) = P(B|A_i) · P(A_i) / Σ P(B|A_j) · P(A_j)

## Independence
- Events A and B are independent if P(A ∩ B) = P(A) · P(B)
- Equivalently: P(A|B) = P(A)

## Permutations & Combinations
- P(n,r) = n! / (n-r)!  (ordered arrangements)
- C(n,r) = n! / (r!(n-r)!)  (unordered selections)
- C(n,r) = C(n, n-r)
- C(n,0) = C(n,n) = 1

## Distributions
### Binomial Distribution
- P(X = k) = C(n,k) · p^k · (1-p)^(n-k)
- Mean: μ = np
- Variance: σ² = np(1-p)

### Poisson Distribution
- P(X = k) = e^(-λ) · λ^k / k!
- Mean = Variance = λ

## Expected Value and Variance
- E[X] = Σ x_i · P(X = x_i)
- Var(X) = E[X²] - (E[X])²
- Var(aX + b) = a² · Var(X)
- E[aX + b] = a · E[X] + b

## Total Probability Theorem
P(B) = Σ P(B|A_i) · P(A_i) for partition {A_1, A_2, ..., A_n}
