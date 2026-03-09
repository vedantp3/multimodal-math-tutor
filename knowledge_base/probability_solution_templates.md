# Probability Solution Templates

## Template: Basic Probability Calculation
**Step 1**: Define the sample space S and count |S|
**Step 2**: Define the event A (favorable outcomes)
**Step 3**: Count |A| using counting principles (multiplication rule, combinations, etc.)
**Step 4**: Calculate P(A) = |A| / |S|
**Step 5**: Simplify and verify 0 ≤ P(A) ≤ 1
**Check**: Verify P(A) + P(A') = 1

## Template: Conditional Probability Problems
**Step 1**: Identify events A and B clearly
**Step 2**: Determine if you need P(A|B) or P(B|A)
**Step 3**: Calculate P(A ∩ B) and P(B)
**Step 4**: Apply P(A|B) = P(A ∩ B) / P(B)
**Step 5**: Verify the result is between 0 and 1
**Common mistake**: Confusing P(A|B) with P(B|A)

## Template: Bayes' Theorem Problems
**Step 1**: Identify the "hypothesis" events (A₁, A₂, ...) and the "evidence" event B
**Step 2**: List all prior probabilities P(Aᵢ)
**Step 3**: List all likelihoods P(B|Aᵢ)
**Step 4**: Calculate total probability P(B) = Σ P(B|Aᵢ)·P(Aᵢ)
**Step 5**: Apply Bayes': P(Aᵢ|B) = P(B|Aᵢ)·P(Aᵢ) / P(B)
**Tip**: Use a tree diagram to organize the information

## Template: Binomial Distribution Problems
**Step 1**: Verify conditions: fixed n trials, two outcomes, constant p, independent trials
**Step 2**: Identify n, p, and the desired k
**Step 3**: Apply P(X = k) = C(n,k) · p^k · (1-p)^(n-k)
**Step 4**: For P(X ≤ k), sum individual probabilities
**Step 5**: Use mean μ = np and variance σ² = np(1-p) if needed

## Template: Permutation/Combination Problems
**Step 1**: Determine if order matters (permutation) or not (combination)
**Step 2**: Check for special conditions (repetition, restrictions)
**Step 3**: Apply the appropriate formula
**Step 4**: Handle restrictions separately (e.g., subtract cases that violate conditions)
**Step 5**: Verify by sanity-checking with small examples
