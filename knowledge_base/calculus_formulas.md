# Calculus Formulas & Identities

## Limits
- lim(x→0) sin(x)/x = 1
- lim(x→0) (1 - cos(x))/x = 0
- lim(x→0) tan(x)/x = 1
- lim(x→0) (eˣ - 1)/x = 1
- lim(x→0) ln(1 + x)/x = 1
- lim(x→∞) (1 + 1/x)ˣ = e
- lim(x→0) (1 + x)^(1/x) = e
- lim(x→a) (xⁿ - aⁿ)/(x - a) = n·a^(n-1)

## L'Hôpital's Rule
If lim f(x)/g(x) gives 0/0 or ∞/∞:
lim f(x)/g(x) = lim f'(x)/g'(x)

## Differentiation Rules
- d/dx [xⁿ] = n·x^(n-1)
- d/dx [eˣ] = eˣ
- d/dx [aˣ] = aˣ · ln(a)
- d/dx [ln(x)] = 1/x
- d/dx [sin(x)] = cos(x)
- d/dx [cos(x)] = -sin(x)
- d/dx [tan(x)] = sec²(x)
- Product rule: d/dx [uv] = u'v + uv'
- Quotient rule: d/dx [u/v] = (u'v - uv')/v²
- Chain rule: d/dx [f(g(x))] = f'(g(x)) · g'(x)

## Integration Rules
- ∫ xⁿ dx = x^(n+1)/(n+1) + C (n ≠ -1)
- ∫ 1/x dx = ln|x| + C
- ∫ eˣ dx = eˣ + C
- ∫ sin(x) dx = -cos(x) + C
- ∫ cos(x) dx = sin(x) + C
- ∫ sec²(x) dx = tan(x) + C
- Integration by parts: ∫ u dv = uv - ∫ v du

## Maxima and Minima
- Find critical points: f'(x) = 0
- Second derivative test: f''(x) > 0 → local minimum, f''(x) < 0 → local maximum
- For constrained optimization: use Lagrange multipliers

## Mean Value Theorem
If f is continuous on [a,b] and differentiable on (a,b):
There exists c in (a,b) such that f'(c) = (f(b) - f(a))/(b - a)

## Definite Integrals Properties
- ∫[a to b] f(x)dx = -∫[b to a] f(x)dx
- ∫[a to b] f(x)dx = ∫[a to c] f(x)dx + ∫[c to b] f(x)dx
- ∫[0 to 2a] f(x)dx = 2∫[0 to a] f(x)dx if f(2a-x) = f(x)
