from sympy import symbol, sympify, simplify, diff, integrate, solve

x = symbols('x')

def process_expression(user_input):
    """
    Takes a math expression as a string, solves it, and returns a dictionary of results.
    :param user_input:
    :return:
    """
    result = {}

    try:
        expression = simpify(user_input)
        result['original'] = expression