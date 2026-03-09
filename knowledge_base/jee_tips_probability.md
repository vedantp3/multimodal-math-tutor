# JEE Tips & Tricks — Probability

## Counting Shortcuts
- **Stars and Bars**: To distribute n identical objects into r groups: C(n+r-1, r-1)
- **Inclusion-Exclusion**: For "at least" problems, use complement: P(at least 1) = 1 - P(none)
- **Circular permutations**: (n-1)! for n objects in a circle
- **Derangements**: D(n) = n!(1 - 1/1! + 1/2! - 1/3! + ... + (-1)ⁿ/n!)

## Conditional Probability Strategies
- **Draw a tree diagram**: Always helps visualize multi-stage problems
- **Two-way tables**: For problems with two categories, organize data in a 2×2 table
- **Check independence first**: If P(A∩B) = P(A)·P(B), use multiplication rule directly

## Distribution Recognition
- **"Exactly k successes in n trials"** → Binomial
- **"First success on kth trial"** → Geometric
- **"Number of events in fixed interval"** → Poisson
- **Problems with "without replacement"** → Hypergeometric

## JEE Probability Problem Patterns
1. **Dice problems**: Total outcomes = 6ⁿ for n dice. Use complementary counting for "at least" problems.
2. **Card problems**: Total = C(52, k). Remember suits, face cards, and their intersections.
3. **Balls in boxes**: Distinguish between identical/distinct balls and boxes. Use appropriate counting method.
4. **Conditional probability chains**: Apply Bayes' theorem with total probability.
5. **Geometric probability**: Probability = favorable area/length ÷ total area/length.

## Quick Verification Methods
- Sum of all probabilities should equal 1
- P(A) + P(A') should equal 1
- Expected value should be "reasonable" given the problem context
- For binomial: mean = np, check if answer is near the expected value
