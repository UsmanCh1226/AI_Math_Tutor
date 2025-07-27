from sympy import symbols, diff, integrate, simplify, sympify, Eq, solve, expand, Function
from sympy.core.mul import Mul
from sympy.core.add import Add
from sympy.core.power import Pow

x = symbols('x')


def solve_expression(parsed):
    """
    Takes parsed input with 'subject', 'expression', and optional 'step_by_step' flag.
    Returns explanation or direct result.
    """

    try:
        expr_str = parsed['expression']
        subject = parsed['subject']
        step_mode = parsed.get('step_by_step', False)

        expr = sympify(expr_str)
        steps = []

        if subject == 'calculus':
            if "differentiate" in expr_str or "derivative" in expr_str:

                derivative = diff(expr, x)

                if not step_mode:
                    return f"Derivative: {derivative}"

                steps.append(f"Original expression: {expr}")
                steps.append("Now let's apply the appropriate rule...")

                if isinstance(expr, Pow):
                    base, exponent = expr.args
                    if base == x:
                        steps.append("This is a power function.")
                        steps.append(f"Use the power rule: d/dx[x^{exponent}] = {exponent}*x^{exponent - 1}")

                elif expr.is_Number:
                    steps.append("This is a constant.")
                    steps.append("The derivative of any constant is 0.")

                elif expr.has(Function):
                    steps.append("This appears to be a composite function.")
                    steps.append("Use the chain rule: d/dx[f(g(x))] = f'(g(x)) * g'(x)")

                elif isinstance(expr, Mul):
                    u, v = expr.args
                    steps.append(f"This is a product of two expressions: {u} * {v}")
                    du = diff(u, x)
                    dv = diff(v, x)
                    steps.append("Use the product rule:")
                    steps.append(f"d/dx[u*v] = u'*v + u*v'")
                    steps.append(f"u = {u}, u' = {du}")
                    steps.append(f"v = {v}, v' = {dv}")
                    steps.append(f"Result: {du}*{v} + {u}*{dv}")

                elif isinstance(expr, Add):
                    terms = expr.args
                    steps.append("This is a sum of terms.")
                    for i, term in enumerate(terms):
                        dterm = diff(term, x)
                        steps.append(f"d/dx of term {i+1} ({term}) = {dterm}")

                else:
                    steps.append("Using general symbolic differentiation.")

                steps.append(f"Final derivative: {derivative}")
                return "\n".join(steps)


            elif "integrate" in expr_str or "antiderivative" in expr_str:
                integral = integrate(expr, x)

                if not step_mode:
                    return f"Integral: {integral} + C"

                steps.append(f"Original expression: {expr}")
                steps.append("Finding the antiderivative with respect to x.")

                if isinstance(expr, Pow) and expr.args[0] == x:
                    n = expr.args[1]
                    steps.append("This is a power of x.")
                    steps.append(f"Use the rule: ∫x^{n} dx = x^{n+1}/({n+1}) + C")

                elif expr.is_Number:
                    steps.append("This is a constant.")
                    steps.append(f"Use the rule: ∫c dx = c*x + C")

                steps.append(f"Final integral: {integral} + C")
                return "\n".join(steps)

        elif subject == 'algebra':
            if "=" in expr_str:
                lhs, rhs = expr_str.split("=")
                equation = Eq(sympify(lhs), sympify(rhs))
                solutions = solve(equation, x)
                if step_mode:
                    steps.append(f"Equation: {lhs} = {rhs}")
                    steps.append("Solving for x using algebraic operations...")
                    steps.append(f"Solution(s): {solutions}")
                    return "\n".join(steps)
                return f"Solution: {solutions}"
            else:
                simplified = simplify(expr)
                if step_mode:
                    steps.append(f"Original expression: {expr}")
                    steps.append("Applying simplification rules...")
                    steps.append(f"Result: {simplified}")
                    return "\n".join(steps)
                return f"Simplified: {simplified}"

        return "Sorry, I can't solve this type of problem yet."

    except Exception as e:
        return f"Error while solving: {e}"
