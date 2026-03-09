# JEE Tips & Tricks — Calculus

## Limit Evaluation Shortcuts
- **Standard limits to memorize**: sin(x)/x → 1, (eˣ-1)/x → 1, ln(1+x)/x → 1
- **1^∞ form**: For lim f(x)^g(x), if f→1 and g→∞, result = e^(lim g(x)·(f(x)-1))
- **0/0 form shortcut**: Before L'Hôpital, try factoring or rationalizing — often faster
- **Squeeze theorem**: Useful for oscillatory limits like x·sin(1/x)

## Differentiation Tricks
- **Implicit differentiation**: When y is defined implicitly, differentiate both sides w.r.t. x and solve for dy/dx
- **Logarithmic differentiation**: For y = f(x)^g(x), take ln both sides: ln(y) = g(x)·ln(f(x))
- **Parametric curves**: dy/dx = (dy/dt)/(dx/dt)

## Integration Shortcuts for JEE
- **Partial fractions**: Always factor denominator first, use coverup method for speed
- **King's Property**: ∫₀ᵃ f(x)dx = ∫₀ᵃ f(a-x)dx — extremely useful for definite integrals
- **Even/Odd functions**: ∫₋ₐᵃ f(x)dx = 2∫₀ᵃ f(x)dx if f is even, = 0 if f is odd
- **Wallis' Formula**: For ∫₀^(π/2) sinⁿ(x)dx patterns

## Optimization Problem Strategy
1. Draw a diagram (always)
2. Express quantity to optimize as single-variable function
3. Find critical points and check endpoints
4. Verify with second derivative test

## Common JEE Calculus Traps
- Not checking if a function is continuous before integrating
- Forgetting to change limits during u-substitution
- Assuming local extrema are global extrema without checking domain
