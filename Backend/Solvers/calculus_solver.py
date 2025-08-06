from sympy import symbols, diff, integrate, sympify, Function
from sympy.core.mul import Mul
from sympy.core.add import Add
from sympy.core.power import Pow

x = symbols('x')


def solve_calculus(expression_str, step_by_step=False):
    steps = []

    try:
        expr = sympify(expression_str)

        if "differentiate" in expression_str or "derivative" in expression_str:
            derivative = diff(expr, x)

            if not step_by_step:
                return f"Derivative: {derivative}"

            steps.append(f"Expression: {expr}")
            steps.append("Applying differentiation rules...")

            if isinstance(expr, Pow):
                base, exponent = expr.args
                if base == x:
                    steps.append("Detected a power function.")
                    steps.append(f"Using Power Rule: d/dx[x^{exponent}] = {exponent}*x^{exponent - 1}")

            elif expr.is_Number:
                steps.append("This is a constant. Derivative of a constant is 0.")

            elif expr.has(Function):
                steps.append("Composite function detected. Apply Chain Rule if needed.")

            elif isinstance(expr, Mul):
                u, v = expr.args
                du = diff(u, x)
                dv = diff(v, x)
                steps.append(f"Product Rule: d/dx[u*v] = u'*v + u*v'")
                steps.append(f"u = {u}, u' = {du}")
                steps.append(f"v = {v}, v' = {dv}")
                steps.append(f"Result: {du}*{v} + {u}*{dv}")

            elif isinstance(expr, Add):
                terms = expr.args
                steps.append("Sum Rule: d/dx[f + g] = f' + g'")
                for i, term in enumerate(terms):
                    dterm = diff(term, x)
                    steps.append(f"Term {i+1}: d/dx({term}) = {dterm}")

            else:
                steps.append("General differentiation applied.")

            steps.append(f"Final Derivative: {derivative}")
            return "\n".join(steps)

        elif "integrate" in expression_str or "antiderivative" in expression_str:
            integral = integrate(expr, x)

            if not step_by_step:
                return f"Integral: {integral} + C"

            steps.append(f"Expression: {expr}")
            steps.append("Applying integration rules...")

            if isinstance(expr, Pow) and expr.args[0] == x:
                n = expr.args[1]
                steps.append("Power Rule for Integration: ∫x^n dx = x^(n+1)/(n+1) + C")

            elif expr.is_Number:
                steps.append(f"Constant Rule: ∫c dx = c*x + C")

            steps.append(f"Final Integral: {integral} + C")
            return "\n".join(steps)

        return "Unrecognized calculus operation."

    except Exception as e:
        return f"Error during calculus solving: {e}"
