# Common Mistakes in Calculus

## Mistake 1: Forgetting the Chain Rule
**Wrong**: d/dx [sin(3x)] = cos(3x)
**Correct**: d/dx [sin(3x)] = 3cos(3x)
**Tip**: When differentiating a composite function, always multiply by the derivative of the inner function.

## Mistake 2: Incorrect Application of L'Hôpital's Rule
**Wrong**: Applying L'Hôpital to limits that are not in 0/0 or ∞/∞ form.
**Correct**: L'Hôpital's Rule only applies to indeterminate forms 0/0 or ∞/∞.
**Tip**: Always check the form of the limit before applying L'Hôpital.

## Mistake 3: Forgetting the Constant of Integration
**Wrong**: ∫ 2x dx = x²
**Correct**: ∫ 2x dx = x² + C
**Tip**: In indefinite integrals, always add the constant C. In definite integrals, C cancels out.

## Mistake 4: Wrong Limits in Definite Integrals After Substitution
**Wrong**: Substituting u = g(x) but keeping original x-limits.
**Correct**: When substituting, convert limits too: x = a → u = g(a), x = b → u = g(b).
**Tip**: Either change limits with substitution or convert back to x before evaluating.

## Mistake 5: Confusing Maxima/Minima Conditions
**Wrong**: f'(x) = 0 always means x is a maximum or minimum.
**Correct**: f'(x) = 0 gives critical points, which could also be inflection points. Use second derivative test.
**Tip**: Always verify with f''(x). If f''(x) = 0, use higher-order derivatives or interval testing.

## Mistake 6: Incorrect Product Rule Application
**Wrong**: d/dx [f(x)·g(x)] = f'(x)·g'(x)
**Correct**: d/dx [f(x)·g(x)] = f'(x)·g(x) + f(x)·g'(x)
**Tip**: The product rule involves two terms, not just the product of derivatives.

## Mistake 7: Not Checking Continuity for Definite Integrals
**Wrong**: Integrating ∫[−1 to 1] 1/x² dx = [-1/x] from -1 to 1 = -2
**Correct**: The function 1/x² has a discontinuity at x = 0, so the integral diverges.
**Tip**: Always check if the integrand is continuous on the interval.
