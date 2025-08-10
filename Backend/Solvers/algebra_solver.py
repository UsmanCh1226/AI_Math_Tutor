from sympy import symbols, Eq, solve, simplify, sympify
from sympy.parsing.sympy_parser import parse_expr
import re

def solve_algebra(expr_str, step_by_step=False, solve_for=None):
    """
    Solves an algebraic equation, supports multiple variables.

    Args:
        expr_str (str): A string like '2*x + y = 5'
        step_by_step (bool): If True, return explanation steps
        solve_for (str or None): variable name to solve for, e.g. 'x' or 'y'

    Returns:
        str or list: solution or steps as explanation
    """
    try:
        if '=' not in expr_str:
            return "Equation must include '='"

        left, right = expr_str.split('=')
        left_expr = parse_expr(left.strip())
        right_expr = parse_expr(right.strip())
        equation = Eq(left_expr, right_expr)

        # Get all symbols (variables) in the equation
        variables = list(equation.free_symbols)
        if not variables:
            return "No variables found to solve for."

        if solve_for:
            solve_var = symbols(solve_for)
        else:
            solve_var = variables

        solutions = solve(equation, solve_var)

        if step_by_step:
            steps = []
            steps.append(f"Step 1: Original equation: {left_expr} = {right_expr}")
            simplified_left = simplify(left_expr)
            simplified_right = simplify(right_expr)
            steps.append(f"Step 2: Simplify both sides: {simplified_left} = {simplified_right}")
            steps.append(f"Step 3: Solving for variable(s): {solve_var}")
            steps.append(f"Solution: {solutions}")
            return steps

        return solutions

    except Exception as e:
        return f"Error solving equation: {str(e)}"
