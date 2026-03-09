# Common Mistakes in Probability

## Mistake 1: Confusing P(A|B) with P(B|A)
**Wrong**: Assuming P(disease|positive test) = P(positive test|disease)
**Correct**: These are different. Use Bayes' Theorem to convert between them.
**Tip**: Always clearly identify which event is the condition and which is what you're computing.

## Mistake 2: Adding Probabilities for Non-Mutually-Exclusive Events
**Wrong**: P(A ∪ B) = P(A) + P(B)
**Correct**: P(A ∪ B) = P(A) + P(B) - P(A ∩ B) — must subtract the overlap.
**Tip**: Only use simple addition when events are mutually exclusive (A ∩ B = ∅).

## Mistake 3: Confusing Combinations and Permutations
**Wrong**: Using P(n,r) when order doesn't matter.
**Correct**: Use C(n,r) for selections and P(n,r) for arrangements.
**Tip**: Ask "does the order of selection matter?" — if no, use combinations.

## Mistake 4: Assuming Independence Without Justification
**Wrong**: Treating events as independent when they are dependent.
**Correct**: Verify independence: P(A ∩ B) = P(A)·P(B) or P(A|B) = P(A).
**Tip**: Sampling without replacement creates dependent events. Drawing with replacement creates independent events.

## Mistake 5: Incorrect Complementary Counting
**Wrong**: P(at least one) = 1 - P(exactly one)
**Correct**: P(at least one) = 1 - P(none)
**Tip**: "At least one" means EVERYTHING except "none at all."

## Mistake 6: Forgetting Total Probability in Bayes' Theorem
**Wrong**: Skipping the denominator in Bayes' formula.
**Correct**: The denominator P(B) = Σ P(B|Aᵢ)·P(Aᵢ) must account for all partitions.
**Tip**: Always enumerate all hypothesis/partition events and compute total probability.

## Mistake 7: Misapplying Binomial Distribution Conditions
**Wrong**: Using binomial distribution when trials are not independent.
**Correct**: Verify: fixed n, two outcomes, constant p, and independent trials.
**Tip**: For "without replacement" problems, use hypergeometric distribution instead.
