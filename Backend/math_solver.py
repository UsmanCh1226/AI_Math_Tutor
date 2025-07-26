from sympy import symbols, diff, integrate, simplify, sympify

x = symbols('x')


def solve_expression(parsed):
    """
        Takes parsed input with 'subject' and 'expression',
        returns a solution string using SymPy.
        """

    try:
        expr = sympify(parsed['expression'])
        if parsed['subject'] == 'calculus':
            if "differentiate" in parsed['expression']:
                return str(diff(expr, x))
            elif "integrate" in parsed['expression']:
                return str(integrate(expr, x))

        elif parsed['subject'] == 'algebra':
            return str(simplify(expr))

        return "Sorry, I can't solve this type of problem yet."

    except Exception as e:
        return f"Error while solving: {e}"
    

def process_expression(user_input):
    """
    Takes a math expression (like 'x**2 + 2*x + 1') as a string,
    performs symbolic math operations on it, and returns the results.

    :param user_input: A string containing a math expression
    :return: A dictionary with the original, simplified, derivative,
             integral, and solution (if possible)
    """
    result = {}

    try:
        expression = sympify(user_input)

        result['original'] = str(expression)

        result['simplified'] = str(simplify(expression))

        result['derivative'] = str(diff(expression, x))

        result['integral'] = str(integrate(expression, x))

        try:
            solutions = solve(expression, x)
            result['solution'] = [str(sol) for sol in solutions]
        except Exception as e:
            result['solution'] = f"Could not solve: {e}"

    except Exception as e:
        result['error'] = f"Invalid input: {e}"

    return result
