"""
math_engine.py
--------------
Routes parsed problems (single-step or pipeline) to the correct solver(s).
"""

from Solvers.algebra_solver import solve_algebra
from Solvers.calculus_solver import solve_calculus
from Solvers.geometry_solver import solve_geometry
from Solvers.stats_solver import solve_statistics


def _call_solver(step: dict, step_by_step: bool) -> str:
    """
    Wrap each solver call so we can pass operation hints when useful.
    Some solvers infer from expression; we optionally prefix operation keywords.
    """
    subject = (step.get("subject") or "").lower()
    operation = (step.get("operation") or "").lower()
    expression = step.get("expression", "")
    parsed = {
        "subject": subject,
        "expression": expression,
        "step_by_step": step_by_step
    }

    # For calculus, many solvers check keywords inside 'expression'
    if subject == "calculus":
        if operation == "differentiate":
            parsed["expression"] = f"differentiate {expression}"
        elif operation == "integrate":
            parsed["expression"] = f"integrate {expression}"
        return solve_calculus(parsed)

    # Algebra solver already distinguishes '=' vs expression and can simplify
    if subject == "algebra":
        # Optionally hint the operation in expression for clarity (non-breaking)
        if operation in {"simplify", "expand", "factor", "solve"} and operation not in expression.lower():
            parsed["expression"] = f"{expression}"
        return solve_algebra(parsed)

    if subject == "geometry":
        # Geometry solver looks for keywords like area/perimeter/volume in expression
        if operation and operation not in expression.lower():
            parsed["expression"] = f"{operation} {expression}"
        return solve_geometry(parsed)

    if subject == "statistics":
        # Stats solver looks for 'mean/median/variance/std/probability' in expression
        if operation and operation not in expression.lower():
            parsed["expression"] = f"{operation} of {expression}"
        return solve_statistics(parsed)

    return "Sorry, I don't know how to solve that type of problem yet."


def route_math_problem(parsed: dict) -> str:
 
    step_by_step = parsed.get("step_by_step", False)

    # Pipeline path
    if "pipeline" in parsed and isinstance(parsed["pipeline"], list):
        outputs = []
        for i, step in enumerate(parsed["pipeline"], 1):
            res = _call_solver(step, step_by_step)
            outputs.append(f"Step {i}: {res}")
        return "\n\n".join(outputs)

    # Single-step path
    return _call_solver(parsed, step_by_step)
